# -*- coding: utf-8 -*-

"""Launch routines."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import logging
import os.path as op
from pprint import pformat
import shutil

import numpy as np

from .traces import SpikeDetekt
from .kwik.creator import create_kwik, KwikCreator
from .kwik.model import KwikModel
from .klustakwik import klustakwik
from .utils import _ensure_dir_exists

logger = logging.getLogger(__name__)


#------------------------------------------------------------------------------
# Launch
#------------------------------------------------------------------------------

def detect(model, interval=None, **kwargs):
    traces = model.all_traces

    # Setup the temporary directory.
    expdir = op.dirname(model.kwik_path)
    sd_dir = op.join(expdir, '.spikedetekt')
    _ensure_dir_exists(sd_dir)

    # Default interval.
    if interval is not None:
        (start_sec, end_sec) = interval
        sr = model.sample_rate
        interval_samples = (int(start_sec * sr),
                            int(end_sec * sr))
    else:
        interval_samples = None

    # Take the parameters in the Kwik file, coming from the PRM file.
    params = model.metadata
    params.update(kwargs)
    # Pretty print params.
    p_params = pformat(params)
    logger.info("Parameters: %s", p_params)

    # Probe parameters required by SpikeDetekt.
    params['probe_channels'] = model.probe.channels_per_group
    params['probe_adjacency_list'] = model.probe.adjacency

    # Start the spike detection.
    logger.debug("Running SpikeDetekt...")
    sd = SpikeDetekt(tempdir=sd_dir, **params)
    out = sd.run_serial(traces, interval_samples=interval_samples)
    return out


def cluster(model, spike_ids=None, **kwargs):
    """Return the spike_clusters and metadata.

    Doesn't make any change to the model. The caller must add the clustering.

    """
    # Skip if no spikes.
    if not model.n_spikes:
        return np.array([], dtype=np.int32), {}

    # Setup the temporary directory.
    expdir = op.dirname(model.kwik_path)
    kk_dir = op.join(expdir, '.klustakwik2')
    _ensure_dir_exists(kk_dir)

    # Take KK's default parameters.
    from klustakwik2.default_parameters import default_parameters
    params = default_parameters.copy()
    # Update the PRM ones, by filtering them.
    params.update({k: v for k, v in model.metadata.items()
                   if k in default_parameters})
    # Update the ones passed to the function.
    params.update(kwargs)

    # Original spike_clusters array.
    if model.spike_clusters is None:
        n_spikes = (len(spike_ids) if spike_ids is not None
                    else model.n_spikes)
        spike_clusters_orig = np.zeros(n_spikes, dtype=np.int32)
    else:
        spike_clusters_orig = model.spike_clusters.copy()

    def on_iter(sc):
        # Update the original spike clusters.
        spike_clusters = spike_clusters_orig.copy()
        spike_clusters[spike_ids] = sc
        # Save to a text file.
        path = op.join(kk_dir, 'spike_clusters.txt')
        # Backup.
        if op.exists(path):
            shutil.copy(path, path + '~')
        np.savetxt(path, spike_clusters, fmt='%d')

    logger.info("Running KK...")
    # Run KK.
    sc, params = klustakwik(model=model, spike_ids=spike_ids,
                            iter_callback=on_iter)
    logger.info("The automatic clustering process has finished.")

    # Save the results in the Kwik file.
    spike_clusters = spike_clusters_orig.copy()
    spike_clusters[spike_ids] = sc

    # Set the new clustering metadata.
    metadata = {'klustakwik2_{}'.format(name): value
                for name, value in params.items()}

    return sc, metadata


def klusta(prm_file,
           output_dir=None,
           do_detect=True,
           do_cluster=True,
           interval=None,
           channel_group=None):
    # Ensure the kwik file exists. Doesn't overwrite it if it exists.
    kwik_path = create_kwik(prm_file=prm_file, output_dir=output_dir)

    # Detection.
    if do_detect:
        # NOTE: always detect on all shanks.
        model = KwikModel(kwik_path)
        out = detect(model, interval=interval)
        model.close()

        # Add the spikes to the kwik file.
        creator = KwikCreator(kwik_path)
        creator.add_spikes_after_detection(out)

    # List of channel groups.
    if channel_group is None:
        channel_groups = out.groups
    else:
        channel_groups = [channel_group]

    # Clustering.
    if do_cluster:
        # Cluster every channel group.
        for channel_group in channel_groups:
            model = KwikModel(kwik_path, channel_group=channel_group)
            logger.info("Clustering group %d (%d spikes).",
                        channel_group, model.n_spikes)
            # Skip clustering if there are no spikes.
            if not model.n_spikes:
                continue
            spike_clusters, metadata = cluster(model)
            model.close()

            # Add the results to the kwik file.
            model = KwikModel(kwik_path, channel_group=channel_group)
            model.add_clustering('main', spike_clusters)
            model.copy_clustering('main', 'original')
            model.clustering_metadata.update(metadata)
            model.close()

    return kwik_path

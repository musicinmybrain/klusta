# -*- coding: utf-8 -*-

"""Test launcher."""

#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import os.path as op

from pytest import fixture

from ..launch import detect, cluster
from ..datasets import download_test_data
from ..kwik.creator import create_kwik, KwikCreator
from ..kwik.mock import mock_prm
from ..kwik.model import KwikModel


#------------------------------------------------------------------------------
# Fixtures
#------------------------------------------------------------------------------

@fixture
def kwik_path(tempdir):
    # Create empty kwik from mock PRM, PRB, and test dat file.
    dat_path = download_test_data('test-32ch-10s.dat')
    kwik_path = op.join(tempdir, 'test-32ch-10s.kwik')
    prm = mock_prm(dat_path)
    create_kwik(prm=prm, kwik_path=kwik_path)
    return kwik_path


#------------------------------------------------------------------------------
# Tests
#------------------------------------------------------------------------------

def test_launch(kwik_path):
    creator = KwikCreator(kwik_path)

    # Detection.
    model = KwikModel(kwik_path)
    out = detect(model, interval=(0, 1))
    model.close()

    # Add spikes in the kwik file.
    creator.add_spikes_after_detection(out)

    # Clustering.
    model = KwikModel(kwik_path)
    assert model.channel_group == 0
    assert model.n_spikes >= 100
    spike_clusters, metadata = cluster(model)
    # Add a new clustering and switch to it.
    model.add_clustering('main', spike_clusters)
    model.copy_clustering('main', 'original')
    model.clustering_metadata.update(metadata)
    model.close()

    # Check.
    model = KwikModel(kwik_path)
    assert model.n_clusters >= 5
    model.describe()

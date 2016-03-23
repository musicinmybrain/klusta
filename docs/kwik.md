# Kwik format

This page describe the Kwik format.

## Quick start with MATLAB

You can open Kwik files in recent versions of MATLAB (they have [native support for HDF5](http://www.mathworks.fr/fr/help/matlab/hdf5.html)).

To read the spike times and cluster numbers, type (`filename` is the `.kwik` file):

```matlab
hdf5read(filename, '/channel_groups/0/spikes/time_samples');
hdf5read(filename, '/channel_groups/0/spikes/clusters/main');
```

The `channel_group` number is the shank number (indexing starts at 0).

## Data files

All files are HDF5 files.

  * The data is stored in the following files:

      * the **KWIK** file is the main file, it contains:
          * all metadata
          * spike times
          * clusters
          * recording for each spike time
          * probe-related information
          * information about channels
          * information about cluster groups
          * events, event_types
          * aesthetic information, user data, application data
      * the **KWX** file contains the masks and features of every spike

  * Once spike sorting is finished, one can discard the KWX file and just keep the KWIK file for subsequent analysis (where spike sorting information like masks and features are not necessary).


### KWIK

Below is the structure of the KWIK file.Everything is a group, except fields with a star (*) which are either leaves (datasets: arrays or tables) or attributes of their parents.

[X] is 0, 1, 2...

    /kwik_version* [=2]
    /name*
    /application_data
        spikedetekt
            MY_SPIKEDETEKT_PARAM*
            ...
    /channel_groups
        [X]  # Absolute channel group index from 0 to Nchannelgroups-1
            name*
            channel_order*  # ordered list of channels, as specified in the PRB file
            adjacency_graph* [Kx2 array of integers]
            application_data
            channels
                [X]  # Relative channel index from 0 to shanksize-1
                    name*
                    ignored*
                    position* (a pair (x, y) in microns relative to the whole multishank probe)
                    voltage_gain* (a float32 number, in microvolts)
                    display_threshold*
                    application_data
                        spikedetekt
            spikes
                time_samples* [N-long EArray of UInt64]
                time_fractional* [N-long EArray of UInt8]
                recording* [N-long EArray of UInt16]
                clusters
                    main* [N-long EArray of UInt32]
                    original* [N-long EArray of UInt32]
                features_masks
                    hdf5_path* [='{kwx}/channel_groups/X/features_masks']
                waveforms_raw
                    hdf5_path* [='{kwx}/channel_groups/X/waveforms_raw']
                waveforms_filtered
                    hdf5_path* [='{kwx}/channel_groups/X/waveforms_filtered']
            clusters
                [clustering_name]
                    [X]  # Cluster number from 0 to Nclusters-1 (unique within a given channel group & clustering name)
                        cluster_group*
                        mean_waveform_raw*
                        mean_waveform_filtered*
                        quality_measures
                            isolation_distance*
                            matrix_isolation*
                            refractory_violation*
                            amplitude*
                            ...
            cluster_groups
                [clustering_name]
                    [X]  # Cluster group number
                        name*
    /recordings
        [X]  # Recording index from 0 to Nrecordings-1
            name*
            start_time*
            start_sample*
            sample_rate*
            bit_depth*
            band_high*
            band_low*
            raw
                hdf5_path* [='{raw.kwd}/recordings/X']
            high
                hdf5_path* [='{high.kwd}/recordings/X']
            low
                hdf5_path* [='{low.kwd}/recordings/X']

### KWX

The **KWX** file contains spike-sorting-related information.

    /kwik_version* [=2]
    /channel_groups
        [X]
            features_masks* [(N x NFEATURES x 2) EArray of Float32]

# Spike sorting with klusta

Let's see how to run klusta on your data.


## Preparing your files

You need to specify three pieces of information in order to run klusta:

* The raw data file(s)
* The probe (PRB) file
* The parameters (PRM) file

**Note: you shouldn't run more than one spike sorting session in a given directory. Use a different directory for every dataset.**


### Raw data

Your raw data needs to be stored in one or several flat binary files with no header (support for files with headers is coming soon). The extension is generally `.dat` but it could be something else.

Typically, the data type is int16 or uint16. The bytes need to be arranged as follows:

```
t0ch0 t0ch1 t0ch2 ... t0chN t1ch0 t1ch1 t1ch2 ...```
```

Channel moves first, time second. Using the Python/NumPy convention, this corresponds to a `(n_samples, n_channels)` array stored in C order. NumPy can read this file efficiently with `np.memmap(dat_path, dtype=dtype, shape=(n_samples, n_channels))` (memory mapping allows to only load what you need in RAM).

You can have several successive files (also known as **recordings** in klusta) for your experiment. They will be virtually concatenated by `klusta`. The offsets will be preserved in the output files.

### Probe file

You need to specify the layout of your probe in a Python file. This file contains a few fields:

* **The list of channels**: typically this is just `0, 1, 2, ..., N`, but you can omit dead or ignored channels.
* **The adjacency graph** of channels that are closed to each other on the probe. This will be used in the spike detection process.
* **The 2D coordinates of the channels** on the probe (optional, only used for visualization purposes).

Here is an example:

```
channel_groups = {
    # Shank index.
    0:
        {
            # List of channels to keep for spike detection.
            'channels': list(range(32)),

            # Adjacency graph. Dead channels will be automatically discarded
            # by considering the corresponding subgraph.
            'graph': [
                (0, 1),
                (0, 2),
                (1, 2),
                (1, 3),
                ...
            ],

            # 2D positions of the channels, only for visualization purposes.
            # The unit doesn't matter.
            'geometry': {
                0: (0, 0),
                1: (10, 20),
                ...
            }
    }
}
```

[The full example is here](https://github.com/kwikteam/klusta/blob/master/klusta/probes/1x32_buzsaki.prb). This is a 32-channel staggered Buzsaki probe. It is already included in klusta, so you can just specify it by its name. We plan to include more built-in probes in the future.

If your probe is not included in klusta, you can just create a new PRB file. Since a PRB file is just a Python file, you can programmatically generate the list of channels or the adjacency graph in the file, instead of typing everything by hand.


### Parameters file

The parameters file is also a Python file. It contains the paths to your raw data files and your PRB file, as well as the metadata related to your data and the spike sorting process.

Here is an example:

```python
experiment_name = 'hybrid_10sec'
prb_file = '1x32_buzsaki'  # or the path to your PRB file

traces = dict(
    raw_data_files=['myrecording.dat', ],  # path to your .dat file(s)
    sample_rate=20000,  # sampling rate in Hz
    n_channels=32,  # number of channels in the .dat files
    dtype='int16',  # the data type used in the .dat files
)

# Parameters for the spike detection process.
spikedetekt = dict(
)

# Parameters for the automatic clustering process.
klustakwik2 = dict(
    num_starting_clusters=100,
)
```

You can specify custom parameters for spike detection and automatic clustering. The default parameters can be found here:

* [Default parameters for spike detection](https://github.com/kwikteam/klusta/blob/master/klusta/traces/default_settings.py)
* [Default parameters for automatic clustering](https://github.com/kwikteam/klustakwik2/blob/master/klustakwik2/default_parameters.py)


## Launching the spike sorting process

We recommend that you use a dedicated directory for every experiment. This directory should contain:

* Your PRM file
* Your PRB file (optional)

Your raw data files can be stored in the directory, or elsewhere, in which case you need to specify the full absolute paths in the PRM file.

Once your directory is ready, launch the spike sorting session with:

```bash
$ klusta yourfile.prm
```

This will generate a .kwik file and a .kwx file with the results.

Type the following to get the list of all options:

```bash
$ klusta --help
```

Here are common options:

* `--output-dir`: the output directory containing the resulting kwik file
* `--detect-only`: only do spike detection.
* `--cluster-only`: only do automatic clustering (spike detection needs to have been done before).
* `--overwrite`: overwrite all previous results.
* `--debug`: display more information about the sorting process.


## Using the GUI

Type the following to open the KlustaViewa GUI on your files once spike sorting has been done:

```bash
klustaviewa yourfile.kwik
```

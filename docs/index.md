# Welcome to klusta

**klusta** is an open source software for automatic spike sorting. It has been designed to scale up to recordings made with probes containing a few dozen channels.


## Overview

As an input, klusta takes a flat binary file containing the analog multi-channel signal. It performs two consecutive steps:

* **Spike detection**: detecting the action potentials across all channels, using a flood-fill algorithm.
* **Automatic clustering**: grouping the spikes into putative neuronal sources. Spikes that look similar are expected to stem from the same neuron.

At the end of the process, you are ready to visualize and fine-tune the data using one of the two GUIs we have developed: **KlustaViewa** (older) or the **Kwik GUI** (newer and experimental).

The entire process has been described [in our paper](http://www.nature.com/neuro/journal/vaop/ncurrent/full/nn.4268.html).


## Installation

[See instructions here](https://github.com/kwikteam/klusta/#quick-install-guide).


## Test dataset

Once installed, you can try the software on test data.

Download and save these two files in a new directory on your computer:

* [Raw data file](http://phy.cortexlab.net/data/samples/hybrid_10sec.dat)
* [Parameter file](http://phy.cortexlab.net/data/samples/hybrid_10sec.prm)

Then, open a terminal in that directory and type the following commands (do not type the `$`):

```bash
$ source activate klusta  # omit the `source` on Windows
$ klusta hybrid_10sec.prm
```

The process should finish after about 20 seconds.


## File format

The results are saved in two new files:

* **A .kwik file**: this file contains all the results of the spike sorting session, except the PCA features: mainly the spike times and spike clusters, and all the metadata.
* **A .kwx file**: this file contains the PCA features.

These files are HDF5 files in the [**Kwik format**](format.md). You can open them with any HDF5 reader and with any programming language.

You can have a quick look inside a `.kwik` file with the following command:

```bash
$ klusta hybrid_10sec.kwik
Kwik file               hybrid_10sec.kwik
Recordings              1
List of shanks          0*
Clusterings             main*, original
Channels                32
Spikes                  1653
Clusters                18
Duration                10s
```


## Using the GUI

You can use one of the two GUIs we have developed to inspect and refine the results manually.

### With KlustaViewa

Type the following:

```bash
klustaviewa hybrid_10sec.kwik
```

### With the phy KwikGUI

Type the following:

```bash
phy kwik-gui hybrid_10sec.kwik --channel-group=0
```

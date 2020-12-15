# Source code folder

All re-usable source code for the project goes here.

The source folder is structured as follows:
```
src
├── __init__.py    <- Makes src a Python module
│
├── constants.py   <- Includes project wide constants for easy imports
│
├── data_loading   <- Scripts to download or generate data
|
├── preprocessing  <- Scripts to turn raw data into clean data and features for modeling
│
├── models         <- Scripts to train models and then use trained models to make
│                     predictions
└── tests          <- Scripts for unit tests of your functions
```

This generic folder structure is useful for most project, but feel free to adapt it to your needs.


To Christina Karamperidou: How do you think that the apparent Pacific double ITCZ cold-tongue bias in CMIP (e.g. Seager et al. NCC 2019, https://doi.org/10.1038/s41558-019-0505-x) might impact your results. Relatedly, out of the two groups of models you made, do you know if one was less biased than the other?





TODO: Feed Pyxpcm modified dataset.

 -      new variable: 'ALL'

 -      Put in configs.

TODO: Check sensitivity to random seed.

 - Look at clusters - see each varies in terms of means and
  covariances.

 - Make 1 colour I-metric plots.

 -  Put Seed in the CONSTANTS file.


TODO: Change IO.

 - Add RUN_NAME

TODO: Possibly back up old data from time-machine.

 - Investigate random seeds within GMM.

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

This generic folder structure is useful for most project, 
but feel free to adapt it to your needs.


TODO: Feed Pyxpcm modified dataset.

 - New variable: 'ALL'.

 - Put in configs.

TODO: Check sensitivity to random seed.

 - Look at clusters - see each varies in terms of means and
  covariances.

 - Make 1 colour I-metric plots.

 - Put Seed in the CONSTANTS file.

TODO: Change IO.

 - Add RUN_NAME.

TODO: Possibly back up old data from time-machine.

 - Investigate random seeds within GMM.

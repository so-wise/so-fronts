# Source code folder

The source folder is structured as follows:

```txt
src
├── __init__.py    <- Makes src a Python module
│
├── constants.py   <- Includes project-wide constants for easy imports.
|                     You should change the main parameters here.
|
├── make_figures.py   <- Makes all the figures in sequences.
|
├── move_figures.py   <- Move the figures to the latex repository.
|
├── time_wrapper.py   <- Add a time wrapper to time most project functions.
│
├── data_loading   <- Scripts to download or generate data
|
├── preprocessing  <- Scripts to turn raw data into clean data and features for modeling
│
├── models         <- Scripts to train models.
|
├── plots         <- Scripts to produce individual plots.
|
├── plot_utils    <- Helper plotting script
|
└── tests          <- Scripts for unit tests of your functions
```

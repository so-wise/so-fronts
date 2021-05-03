# Source code folder

All re-usable source code for the project goes here.

The source folder is structured as follows:

```txt
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

## Reformatting code

Inevitably variables will need to be renamed etc.

One helpful tool is `grep`. An example of using it is:

```bash

grep -R 'cst.TIME_NAME' src

grep -R 'coastlines' src
```

This will list all the instances where the name in question occurs in this repository.

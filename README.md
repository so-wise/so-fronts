# Identifying Southern Ocean fronts using unsupervised classification and edge detection

 [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
 <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## K=5

![I metric for K=5](gifs/boundaries-k5.gif)

## Short description

A `python3` repository which should reproduce `OS022-08` from AGU 2020.

## Requirements

- Python 3.6+ (final run for paper used `python==3.8.8`)
- Anaconda, with `conda` working in shell.
- `pdflatex` for high quality figures (should work without).
- `make` in shell.
- `xarray`, `sklearn`, `cartopy` etc. are the main packages installed.

## Getting started

- Make the environment:

    ```bash
    make env
    ```

- Activate the environment in conda:

     ```bash
     conda activate ./env
     ```

- Make the documentation and load it in your web browser:

    ```bash
    make docs
    ```

- Make your Jupyter notebooks more functional with timings etc.:

    ```bash
    make jupyter_pro
    ```

- To see the other options in the `Makefile` type:

    ```bash
    make help
    ```

- Run tests:

   ```bash
   python -m unittest
   ```

- Download data (`get_zip`  1694.64639 s):

   ```bash
   python3 src/data_loading/bsose_download.py
   ```

- Make I-metric in list:

   ```bash
   python3 src/models/batch_i_metric.py
   ```

## Project Organization

```txt
├── LICENSE
├── Makefile           <- Makefile with commands like `make init` or `make lint-requirements`
├── README.md          <- The top-level README for developers using this project.
|
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
|   |                     the creator's initials, and a short `-` delimited description, e.g.
|   |                     `1.0_jqp_initial-data-exploration`.
│   ├── exploratory    <- Notebooks for initial exploration.
│   └── reports        <- Polished notebooks for presentations or intermediate results.
│
├── report             <- Generated analysis as HTML, PDF, LaTeX, etc.
│   ├── figures        <- Generated graphics and figures to be used in reporting
│   └── sections       <- LaTeX sections. The report folder can be linked to your overleaf
|                         report with github submodules.
│
├── requirements       <- Directory containing the requirement files.
│
├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
├── src                <- Source code for use in this project.
|   |
│   ├── __init__.py    <- Makes src a Python module
|   |
|   ├── configs        <- config files for hydra (e.g. BSOSE coordinates)
│   │
│   ├── data_loading   <- Scripts to download or generate data
│   │
│   ├── simulation     <- Scripts to turn raw data into clean data and features for modeling
|   |
│   ├── plotting       <- plotting
│   │
│   └── tests          <- Scripts for unit tests of your functions
│
└── setup.cfg          <- setup configuration file for linting rules
```

## Code formatting

To automatically format your code, make sure you
have `black` installed (`pip install black`) and call:

```bash

black . 
```

from within the project directory.

## Testing

```bash
python3 -m unittest
```

## K=2

![I metric for K=2](gifs/boundaries-k2.gif)

## K=4

![I metric for K=4](gifs/boundaries-k4.gif)

---

Project template created by the
[Cambridge AI4ER Cookiecutter](https://github.com/ai4er-cdt/ai4er-cookiecutter).

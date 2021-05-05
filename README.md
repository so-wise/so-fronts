# IDefining Southern Ocean fronts using unsupervised classification

 [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
 <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Short description

In the Southern Ocean, fronts delineate water masses, which correspond to upwelling
and downwelling branches of the overturning circulation. Classically, oceanographers
define Southern Ocean fronts as a small number of continuous linear features that
encircle Antarctica. However, modern observational and theoretical developments are
challenging this traditional framework to accommodate more localized views of fronts
[Chapman et al. 2020].

Here we present code for implementing two related methods for calculating fronts from
oceanographic data. The first method uses unsupervised classification (specifically,
Gaussian Mixture Modeling or GMM) and a novel interclass metric to define fronts.
This approach produces a discontinuous, probabilistic view of front location,
emphasising the fact that the boundaries between water masses are not uniformly sharp
across the entire Southern Ocean.

The second method uses Sobel edge detection to highlight rapid changes [Hjelmervik & Hjelmervik, 2019].
This approach produces a more local view of fronts, with the advantage that it can highlight the movement
of individual eddy-like features (such as the Agulhas rings).

## I metric for K=5

![I metric for K=5](gifs/boundaries-k5.gif)


## Getting started

- Make the environment:

    ```bash
    make env
    ```

- Activate the environment in conda:

     ```bash
     conda activate ./env
     ```

- Change the settings in `src.constants` to set download location etc.

- Download data (`get_zip`  1694.64639 s):

   ```bash
   python3 src/data_loading/bsose_download.py
   ```

- Make I-metric:

   ```bash
   python3 src/models/batch_i_metric.py
   ```

- Make figures:
   ```bash
   python3 main.py
   ```

## Project Organization

```txt
├── LICENSE
├── Makefile           <- Makefile with commands like `make env` or `make `
├── README.md          <- The top-level README for developers using this project.
├── main.py            <- The top-level README for developers using this project.
|
├── notebooks          <- Jupyter notebooks. 
|   |
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
│   ├── data           <- KO fronts to plot.
│   │
│   ├── data_loading   <- Scripts to download and name data.
│   │
│   ├── models         <- Make I metric, sobel edge detection.
│   │
│   ├── plot           <- plotting
|   |
│   ├── plot_utils      <- plotting utilities
|   |
|   ├──  tests          <- Scripts for unit tests of your functions
|   | 
|   ├── animate.py       <- animate i metric.
|   ├── constants.py     <- constains majority of run parameters to change.
|   ├── make_figures.py  <- make figures in one long script.
|   ├── move_figures.py  <- move figures script (unnecessary).
|   └── time_wrapper.py  <- time wrapper to time parts of program.
│
└── setup.cfg          <- setup configuration file for linting rules
```

## Requirements

- Python 3.6+ (final run for paper used `python==3.8.8`)
- Anaconda, with `conda` working in shell.
- `pdflatex` for high quality figures (should work without).
- `make` in shell.
- `xarray`, `sklearn`, `cartopy` etc. are the main packages installed.

---

Project template created by the
[Cambridge AI4ER Cookiecutter](https://github.com/ai4er-cdt/ai4er-cookiecutter).

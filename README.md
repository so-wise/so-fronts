# Identifying Southern Ocean fronts using unsupervised classification and edge detection

 [![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
 <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## Short description

A `python3` repository which should reproduce `OS022-08` from AGU 2020.

## Requirements

- Python 3.8+
- Anaconda, with `conda` working in shell.
- `pdflatex` for high quality figures (should still work without).

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

## Reformatting code

Inevitably variables will need to be renamed etc.

One helpful tool is `grep`. An example of using it is:

```bash
grep -R 'cst.TIME_NAME' src
```

This will list all the instances where the name in question occurs in this repository.

## Documentation formatting

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## Commands

- `mkdocs new [dir-name]` - Create a new project.
- `mkdocs serve` - Start the live-reloading docs server.
- `mkdocs build` - Build the documentation site.
- `mkdocs -h` - Print help message and exit.

## Project layout

```txt
    mkdocs.yml    # The configuration file.
    docs/
        index.md  # The documentation homepage.
        ...       # Other markdown pages, images and other files.
```

---

Project template created by the
[Cambridge AI4ER Cookiecutter](https://github.com/ai4er-cdt/ai4er-cookiecutter).

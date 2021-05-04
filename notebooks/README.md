# Notebooks

## Structure

Exploratory notebooks for initial explorations go into the `notebooks/exploratory` folder.
Polished work for reporting and demonstration purposes goes into `notebooks/reports`

## Useful initialization cell

To avoid having to reload the notebook when you change code from underlying imports, we recommend the following handy initialization cell for jupyter notebooks:

```txt
%load_ext autoreload             # loads the autoreload package into ipython kernel
%autoreload 2                    # sets autoreload mode to automatically reload modules when they change
%config IPCompleter.greedy=True  # enables tab completion
```


# japan2011_transect

See ../README.md for general info on version of Clawpack needed.

To run the following:


```
    python maketopo.py  # to fetch topo and extract transect

    python make_figures.py # to run code and make plots for Figure 9
```

Note that `make_figures.py` has a boolean variable `run_code`. Set this to
`True` if you have not yet run the code via `make .output`.

After running the code you can also 

```
    make plots
```
to create plots of all frames.

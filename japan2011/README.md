
# japan2011

See ../README.md for general info on version of Clawpack needed.

To run the following:


```
    python maketopo.py  # to fetch topo and dtopo files

    python make_fgmax_transects.py  # to create input files for transect data

    make .output  # to run code, takes several hours

    python plot_planview.py   # to make plan view plots for Figure 7

    python plot_transects # to make transect cross section plots for Figure 8
```

After running the code, you can also 

```
    make plots
```
to create plots of all frames.

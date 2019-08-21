# shoaling_paper_figures

Code to accompany the paper 
*Shoaling on Steep Continental Slopes: Relating Transmission and Reflection Coefficients to Green's Law*, by J. George, D.  I. Ketcheson, and R. J. LeVeque.  

Revised code for the revised paper submitted June, 2019 and then revised
again to improve Japan 2011 figures and submitted in August, 2019.

The figures in the paper were generated using Clawpack Version 5.5.0, [DOI: 10.5281/zenodo.1405834](https://doi.org/10.5281/zenodo.1405834).  See the [documentation](http://www.clawpack.org) for installation instructions.

In addition, the code in `qinit_step` and `qinit_box` requires a 1-dimensional 
version of GeoClaw that is still under development.  This code runs with
commit 00a77888 of the repository https://github.com/clawpack/geoclaw_1d.

See the `README.md` files in each subdirectory for further instructions.

**Figure 1:** topography
`qinit_step/make_plots_for_paper.py`

**Figures 2, 3:** square pulse on different slopes
`qinit_box/make_figures.py`

**Figure 4:** layered media (topo and x-t plane):
`layers.py`

**Figure 5:** evolution of step function data:
`qinit_step/make_plots_for_paper.py`

**Figure 6:** sum of positive and negative steps:
`qinit_step/combine_steps.py`

**Figure 7:** Tohoku simulation, plan view plots:
`japan2011/plot_planview.py`

**Figure 8:** Tohoku simulation, transect plots:
`japan2011/plot_transects.py`

**Figure 9:** One dimensional code run on transect:
`japan2011_transect/make_figures.py`

The directory `figures` contains the figures created by the 
steps outlined above.


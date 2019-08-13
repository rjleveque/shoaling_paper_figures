
from __future__ import print_function
from pylab import *
import os

from clawpack.clawutil.runclaw import runclaw
from clawpack.visclaw.frametools import plotframe

from clawpack.visclaw.data import ClawPlotData
import makegrid
import mapc2p
import setplot

run_code = False  # set to False if output already exists
if run_code:
    # create executable and .data files:
    os.system('make .exe')
    os.system('make data')

savefig_ext = '.jpg'
figdir = '../figures'
os.system('mkdir -p %s' % figdir)


def save_figure(fname):
    """Save figure to figdir with desired extension"""
    full_fname = os.path.join(figdir,fname) + savefig_ext
    savefig(full_fname, bbox_inches='tight')
    print('Created %s' % full_fname)


makegrid.makegrid()

if run_code:
    runclaw(xclawcmd='xgeo',outdir=outdir)   # run clawpack code

pd = ClawPlotData()
pd = setplot.setplot(pd)  # reload grid.data for each xs value
pd.outdir=os.path.abspath('_output')
for frameno in [0,18]:
    plotframe(frameno,pd)
    fname = 'transect_frame%s' % str(frameno).zfill(2)
    save_figure(fname)

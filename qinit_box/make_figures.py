
from __future__ import print_function
from pylab import *
import os

from clawpack.clawutil.runclaw import runclaw
from clawpack.visclaw.frametools import plotframe

from clawpack.visclaw.data import ClawPlotData
import makegrid
from imp import reload
reload(makegrid)

run_code = True  # set to fault if output already exists
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

for xs in [0., 15e3, 60e3]:
    makegrid.makegrid(xs)
    import mapc2p
    import setplot
    reload(mapc2p)
    reload(setplot)
    xs_str = 'box_xs%s' % str(int(xs/1e3)).zfill(2)
    w_str = 'w%s' % str(int(xs/1e3)).zfill(2)
    outdir = '_output_' + w_str
    print('outdir = ',outdir)
    if run_code:
        runclaw(xclawcmd='xgeo',outdir=outdir)   # run clawpack code
    pd = ClawPlotData()
    pd.outdir = outdir
    pd = setplot.setplot(pd)  # reload grid.data for each xs value
    pd.outdir=os.path.abspath(outdir)
    for frameno in [0,6]:
        plotframe(frameno,pd)
        fname = xs_str + '_frame%s' % str(frameno).zfill(2)
        save_figure(fname)



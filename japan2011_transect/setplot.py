
from __future__ import print_function

import os, sys

from clawpack.geoclaw_1d import geoplot
from imp import reload

import setrun
rundata=setrun.setrun()

import mapc2p
reload(mapc2p)  # in case num_cells changed
from mapc2p import mapc2p


import numpy
from pylab import find

try:
    fname = '_output/fort.hmax'
    d = numpy.loadtxt(fname)
    etamax = numpy.where(d[:,1]>1e-6, d[:,2], numpy.nan)
    #xmax = d[:,0]
    xmax = mapc2p(d[:,0])
    jmax = find(d[:,1]>0).max()
    print("run-in = %8.2f,  run-up = %8.2f" % (d[jmax,0],d[jmax,2]))
    print('Loaded hmax from ',fname)
except:
    xmax = None
    print("Failed to load fort.hmax")

griddata = numpy.loadtxt('grid.data', skiprows=1)
xgrid = griddata[:,0]
zgrid = griddata[:,1]

#xlimits = [-300e3,100e3]
xlimits = [-250,0]

def timeformat(t):
    from numpy import mod
    hours = int(t/3600.)
    tmin = mod(t,3600.)
    min = int(tmin/60.)
    sec = int(mod(tmin,60.))
    timestr = '%s:%s:%s' % (hours,str(min).zfill(2),str(sec).zfill(2))
    return timestr


def setplot(plotdata=None):

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()

    def fixticks1(current_data):
        from pylab import ticklabel_format, grid
        ticklabel_format(format='plain',useOffset=False)
        #grid(True)

    def fixticks(current_data):
        from pylab import ticklabel_format, plot,grid,ones,sqrt,\
             where,tight_layout,legend,nan, title
        ticklabel_format(format='plain',useOffset=False)

        # to plot max elevation over entire computation:
        if xmax is not None:
            plot(xmax, etamax, 'r')

        #grid(True)
        hl = 3000.  #2500.
        hr = 100.    #160.
        greens = (hl/hr)**(0.25)
        print('greens = ',greens)
        z = current_data.q[0,:] - current_data.q[2,:]
        z = where(z>10, z, 10.)
        xp = mapc2p(current_data.x)
        plot(xp, (hl/z)**(0.25),'g--',label='CG')
        #import pdb; pdb.set_trace()
        #plot(xlimits,[greens,greens],'g--')
        ctrans = 2*sqrt(hl)/(sqrt(hl)+sqrt(hr))
        crefl = (sqrt(hl)-sqrt(hr))/(sqrt(hl)+sqrt(hr))
        print('ctrans = ',ctrans)
        print('crefl = ',crefl)
        #plot(xlimits,[crefl,crefl],'c--',label='CR')
        hm = 1400.
        ct12 = 2*sqrt(hl)/(sqrt(hl)+sqrt(hm)) * 2*sqrt(hm)/(sqrt(hm)+sqrt(hr))
        plot([-60e3,0],[ct12,ct12],'r--',label='CT1*CT2')
        #plot([-60e3,0],[ctrans,ctrans],'b--',label='CT')
        ctx = 2*sqrt(hl)/(sqrt(hl)+sqrt(z))
        plot(xp, ctx, 'b--', label='CT')
        #ct12g = where(xp<-50e3, nan, ct12*(hr/z)**(0.25))
        #plot(xp, ct12g, 'm--', label='CT12*G')
        legend(loc='upper left', fontsize=8)
        #tight_layout()
        timestr = timeformat(current_data.t)
        title('Surface displacement at time %s' % timestr)

    plotfigure = plotdata.new_plotfigure(name='domain', figno=10)
    #plotfigure.kwargs = {'figsize':(7,6.5)}
    plotfigure.kwargs = {'figsize':(7,5)}
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'axes([.1,.6,.8,.3])' #'subplot(211)'
    plotaxes.xlimits = xlimits
    #plotaxes.xlimits = [-100e3,-20e3]
    plotaxes.ylimits = [-1,4]
    plotaxes.title = 'Surface displacement'
    plotaxes.afteraxes = fixticks

    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.plot_var = geoplot.surface
    plotitem.plot_var2 = geoplot.topo
    plotitem.color = [.5,.5,1]
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.surface
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    # Topography plot:

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'axes([.1,.1,.8,.3])' #'subplot(212)'
    plotaxes.xlimits = xlimits
    #plotaxes.xlimits = [-100e3,-20e3]
    plotaxes.ylimits = [-3500, 500]
    #plotaxes.title = 'Full depth'
    #plotaxes.title = 'topography'

    def fix_topo_plot(current_data):
        from pylab import title,xlabel
        title('Topography')
        xlabel('kilometers', fontsize=14)
    plotaxes.afteraxes = fix_topo_plot

    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.plot_var = geoplot.surface
    plotitem.plot_var2 = geoplot.topo
    plotitem.color = [.5,.5,1]
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    def deep(current_data):
        from numpy import ones
        x = current_data.x
        z = -10000*ones(x.shape)
        return z

    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.plot_var = geoplot.topo
    plotitem.plot_var2 = deep
    plotitem.color = [.5,1,.5]
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p


    #----------

    plotfigure = plotdata.new_plotfigure(name='shore', figno=1)
    #plotfigure.kwargs = {'figsize':(9,11)}
    plotfigure.show = False
    

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(211)'
    plotaxes.xlimits = [0,80e3]
    plotaxes.ylimits = [-4,4]
    plotaxes.title = 'Zoom on shelf'

    plotaxes.afteraxes = fixticks

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.surface
    #plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    #plotitem.plot_var = geoplot.surface
    #plotitem.plot_var2 = geoplot.topo
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'k'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'subplot(212)'
    #plotaxes.xlimits = [-2000,2000]
    plotaxes.xlimits = [-1000,1000]
    #plotaxes.ylimits = [-10,40]
    plotaxes.ylimits = [-20,60]
    plotaxes.title = 'Zoom around shore'

    plotaxes.afteraxes = fixticks

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = False
    plotitem.plot_var = geoplot.surface

    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.plot_var = geoplot.surface
    plotitem.plot_var2 = geoplot.topo
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'k'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p


    plotdata.printfigs = True          # Whether to output figures
    plotdata.print_format = 'png'      # What type of output format
    plotdata.print_framenos = 'all'      # Which frames to output
    plotdata.print_fignos = 'all'      # Which figures to print
    plotdata.html = True               # Whether to create HTML files
    plotdata.latex = False             # Whether to make LaTeX output
    plotdata.parallel = True

    return plotdata


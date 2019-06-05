
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
    xmax = d[:,0]
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
#xlimits = [-300,100]
xlimits = [-300,150]

def setplot(plotdata=None):

    if plotdata is None:
        from clawpack.visclaw.data import ClawPlotData
        plotdata = ClawPlotData()

    plotdata.clearfigures()

    def fixticks1(current_data):
        from pylab import ticklabel_format, grid
        ticklabel_format(format='plain',useOffset=False)
        grid(True)

    def fixticks(current_data):
        from pylab import ticklabel_format, plot,grid,ones,sqrt, \
            legend,title,ylabel,text
        ticklabel_format(format='plain',useOffset=False)

        # to plot max elevation over entire computation:
        #if xmax is not None:
        #    plot(xmax, etamax, 'r')

        #grid(True)
        hl = 3200.
        hr = 200.
        greens = (hl/hr)**(0.25)
        print('greens = ',greens)
        #plot(current_data.x, greens*ones(current_data.x.shape),'g--')
        plot(xlimits,[greens,greens],'g--', label='$C_g$, Greens Law')
        ctrans = 2*sqrt(hl)/(sqrt(hl)+sqrt(hr))
        crefl = (sqrt(hl)-sqrt(hr))/(sqrt(hl)+sqrt(hr))
        print('ctrans = ',ctrans)
        plot(xlimits,[ctrans,ctrans],'r--', label='$C_T$, Transmission coefficient')
        print('crefl = ',crefl)
        plot(xlimits,[crefl,crefl],'m--', label='$C_R$, Reflection coefficient')
        legend(loc='upper left')
        title('')
        ylabel('meters', fontsize=14)
        if current_data.frameno == 0:
            text(-95,-0.4,'$\longrightarrow$',fontsize=20)
            text(-95,-0.6,'Incident')
        h = current_data.q[0,:]
        mx2 = int(round(len(h)/2.))
        etamax2 = (h[:mx2] - hl).max()
        print('mx2 = %i, etamax2 = %g' % (mx2,etamax2))
        if (current_data.frameno == 5) and (etamax2 > 0.1):
            text(-190,-0.5,'$\longleftarrow$',fontsize=20)
            text(-190,-0.7,'Reflected')
            text(30,-0.5,'$\longrightarrow$',fontsize=20)
            text(15,-0.7,'Transmitted')
        if (current_data.frameno == 6) and (etamax2 > 0.1):
            text(-260,-0.5,'$\longleftarrow$',fontsize=20)
            text(-260,-0.7,'Reflected')
            text(40,-0.5,'$\longrightarrow$',fontsize=20)
            text(25,-0.7,'Transmitted')
        elif (current_data.frameno == 6):
            text(-20,-0.5,'$\longleftarrow$',fontsize=20)
            text(-20,-0.7,'Reflected')
            text(70,-0.5,'$\longrightarrow$',fontsize=20)
            text(65,-0.7,'Transmitted')
        

    plotfigure = plotdata.new_plotfigure(name='domain', figno=0)
    plotfigure.kwargs = {'figsize':(7,6.5)}
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'axes([.1,.4,.8,.5])' #'subplot(211)'
    plotaxes.xlimits = xlimits
    #plotaxes.xlimits = [-100e3,-20e3]
    plotaxes.ylimits = [-1,3]
    plotaxes.title = 'Surface displacement'
    plotaxes.afteraxes = fixticks

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = geoplot.surface
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'k'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.show = False
    plotaxes.axescmd = 'subplot(312)'
    plotaxes.xlimits = xlimits
    #plotaxes.xlimits = [-100e3,-20e3]
    #plotaxes.ylimits = [-1000, 1000]
    #plotaxes.title = 'Full depth'
    plotaxes.title = 'momentum'
    plotaxes.afteraxes = fixticks1
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between')
    plotitem.show = False
    plotitem.plot_var = geoplot.surface
    plotitem.plot_var2 = geoplot.topo
    plotitem.color = 'b'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'k'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    plotitem.plot_var = 1
    plotitem.color = 'k'
    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotaxes = plotfigure.new_plotaxes()
    plotaxes.axescmd = 'axes([.1,.1,.8,.2])' #'subplot(212)'
    plotaxes.xlimits = xlimits
    #plotaxes.xlimits = [-100e3,-20e3]
    #plotaxes.ylimits = [-1000, 1000]
    #plotaxes.title = 'Full depth'
    #plotaxes.title = 'topography'

    def fix_topo_plot(current_data):
        from pylab import title,xlabel
        title('')
        xlabel('kilometers', fontsize=14)
    plotaxes.afteraxes = fix_topo_plot

    plotitem.MappedGrid = True
    plotitem.mapc2p = mapc2p

    plotitem = plotaxes.new_plotitem(plot_type='1d_plot')
    #plotitem.show = False
    plotitem.plot_var = geoplot.topo
    plotitem.color = 'k'
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


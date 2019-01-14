
from pylab import *
import gridtools
from clawpack.pyclaw import Solution
from clawpack.geoclaw import fgmax_tools
import os

outdir = '_output'
format = 'binary'

savefig_ext = '.jpg'
figdir = '../figures'
os.system('mkdir -p %s' % figdir)

def save_figure(fname):
    """Save figure to figdir with desired extension"""
    full_fname = os.path.join(figdir,fname) + savefig_ext
    savefig(full_fname, bbox_inches='tight')
    print('Created %s' % full_fname)


xlimits = [-127, -124]
zlimits = [-0.2, 0.6]

def timeformat(t):
    from numpy import mod
    hours = int(t/3600.)
    tmin = mod(t,3600.)
    min = int(tmin/60.)
    sec = int(mod(tmin,60.))
    timestr = '%s:%s:%s' % (hours,str(min).zfill(2),str(sec).zfill(2))
    return timestr
    
def eta(q):
    eta = where(q[0,:,:]>0, q[3,:,:], nan)
    return eta

def B(q):
    return q[3,:,:]-q[0,:,:]


def plot_transect(ylat, frameno, fg, xcutoff, trname, plotdir):

    figure(20, figsize=(10,3))
    clf()

    xout = linspace(xlimits[0], xlimits[1], 1000)
    yout = ylat*ones(xout.shape)

    framesoln = Solution(frameno, path=outdir, file_format=format)
    eta = gridtools.grid_output_2d(framesoln, 3, xout, yout)
    topo = gridtools.grid_output_2d(framesoln, B, xout, yout)

    fill_between(xout, eta, topo, color=[.5,.5,1])
    fill_between(xout, topo, -10000, color=[.5,1,.5])
    plot(xout, eta, 'b')
    plot(xout, topo, 'g')
    grid(True)

    eta = fg.B + fg.h
    eta_max = where(fg.X < xcutoff, eta, nan)
    plot(fg.X, eta_max, 'r', label='wave height')
    xlim(xlimits)
    ylim(zlimits)
    timestr = timeformat(framesoln.t)
    title('Transect of wave at latitude %.1f at time %s' % (ylat,timestr))
    ticklabel_format(format='plain',useOffset=False)
    #xticks(rotation=20)
    xlabel('Longitude')
    ylabel('meters')
    hl = 3000.
    A0 = 0.1328
    z = where(topo<-10, -topo, nan)
    AG = A0 * (hl/z)**0.25
    plot(xout, AG, 'g--',label="Green's Law")
    ctx = A0 * 2*sqrt(hl)/(sqrt(hl)+sqrt(z))
    plot(xout, ctx, 'b--', label='Transmission')
    legend(loc='upper left')

    fname = '%s_%s' % (trname,str(frameno).zfill(4))
    save_figure(fname)

def plot_topo(fg, trname, plotdir):
    figure(21, figsize=(10,3))
    clf()
    sealevel = where(fg.B<0, 0, nan)
    fill_between(fg.X, fg.B, sealevel, color=[.5,.5,1])
    fill_between(fg.X, fg.B, -10000, color=[.5,1,.5])
    plot(fg.X, sealevel, 'b')
    plot(fg.X, fg.B, 'g')
    grid(True)
    xlim(xlimits)
    ylim(-3500, 500)
    title('Topography on Transect at Latitude %.1f' % ylat)
    ticklabel_format(format='plain',useOffset=False)
    #xticks(rotation=20)
    xlabel('Longitude')
    ylabel('meters')
    fname = '%s_topo' % trname
    save_figure(fname)

    
# Transect at ylat=44.2:

plotdir = '_transects_44_2_new'
trname = 'Transect_44_2'
ylat = 44.2
xcutoff = -124.175

os.system('mkdir -p %s' % plotdir)

fg2 = fgmax_tools.FGmaxGrid()
fg2.read_input_data('fgmax_transect_2.txt')
fg2.read_output(fgno=2,outdir='_output')

frameno = 1
plot_transect(ylat, frameno, fg2, xcutoff, trname, plotdir)

frameno = 2
plot_transect(ylat, frameno, fg2, xcutoff, trname, plotdir)

frameno = 4
plot_transect(ylat, frameno, fg2, xcutoff, trname, plotdir)

plot_topo(fg2, trname, plotdir)



# Transect at ylat=44.4:

plotdir = '_transects_44_4_new'
trname = 'Transect_44_4'
ylat = 44.4
xcutoff = -124.12

os.system('mkdir -p %s' % plotdir)


fg1 = fgmax_tools.FGmaxGrid()
fg1.read_input_data('fgmax_transect_1.txt')
fg1.read_output(fgno=1,outdir='_output')

frameno = 1
plot_transect(ylat, frameno, fg1, xcutoff, trname, plotdir)

frameno = 2
plot_transect(ylat, frameno, fg1, xcutoff, trname, plotdir)

frameno = 4
plot_transect(ylat, frameno, fg1, xcutoff, trname, plotdir)

plot_topo(fg1, trname, plotdir)

from __future__ import print_function

from pylab import *
from scipy.interpolate import interp1d
from interp import pwcubic, pwlinear

def makegrid(xs):
    grav = 9.81

    mx = 10000  # desired number of grid cells

    #xs = 60e3
    x1 = 100e3
    x0 = -3*x1

    x0_shore = x1     # initial shoreline
    x0_slope = -xs     # start of continental slope
    x0_shelf =  xs     # start of continental shelf

    x0_beach = 1e10    # no beach

    z0_ocean = -3200.     # depth of ocean = depth at x0_slope
    z0_shelf = -200.      # depth at x0_shelf
    z0_beach = -200.       # depth at x0_beach
    z0_shore = -200.      # depth at x0_shore

    x1 = x0_shore          # no beach
    #x1 = x0_shore + 2e3   # add onshore beach for runup

    def shelf1(r):
        """
        Ocean followed by continental slope, continental shelf, and beach.
        The ocean is flat, the slope is linear (or could be cubic), 
        and the shelf and beach are linear.
        """

        xi = array([x0, x0_slope, x0_shelf, x0_beach, x0_shore])
        zl = array([z0_ocean, z0_ocean, z0_shelf, z0_beach, z0_shore])
        zr = zl  # continuous!
        slope_of_beach = (z0_beach - z0_shore) / (x0_beach - x0_shore)

        if x0_beach != x0_shelf:
            slope_of_shelf = (z0_beach - z0_shelf) / (x0_beach - x0_shelf)
        else:
            slope_of_shelf = slope_of_beach

        print("Slope of shelf = ",slope_of_shelf)
        print("Slope of beach = ",slope_of_beach)
        slopel = array([0., 0., slope_of_shelf, slope_of_shelf, slope_of_beach])
        sloper = array([0., 0., slope_of_shelf, slope_of_beach, slope_of_beach])
        #z = pwcubic(xi, zl, zr, slopel, sloper, r)
        z = pwlinear(xi, zl, zr, r)
        return z

    # minimum depth, below which uniform grid is used:
    hmin = 50. 
    cmin = sqrt(grav*hmin)

    def c(x):
        z = shelf1(x)
        h = where(-z > hmin, -z, hmin)
        c = sqrt(grav*h)
        return c

    xunif = linspace(x0, x1, 2*mx)
    cunif = c(xunif)
    csum = cumsum(1./cunif)
    csum = csum - csum[0]

    csum = csum / csum[-1]
    cinv = interp1d(csum, xunif)

    xc = linspace(0, 1, mx+1)   # computational grid
    xp = cinv(xc)
    z = shelf1(xp)


    #z = 0.5*(shelf1(xp[1:]) + shelf1(xp[:-1]))
    fname = 'grid.data'
    f = open(fname,'w')
    f.write('%10i \n' % mx)
    for i in range(mx+1):
        f.write('%15.4f %15.4f\n' % (xp[i],z[i]))
    f.close()
    print("Created %s, containing cell edges" % fname)

    if 1:
        figure(1, figsize=(8,4))
        clf()
        fill_between(xp,where(z<0,z,nan),0.,color=[.5,.5,1])
        plot(xp,z,'g')
        xlim(x0,x1)
        ylim(z.min()-500,500)
        fname = 'topo.png'
        savefig(fname)
        print("Created ",fname)

if __name__=='__main__':
    makegrid(xs=15.e3)


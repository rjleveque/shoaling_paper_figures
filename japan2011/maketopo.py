"""
Need to edit based on 
 /Users/rjl/git/GeoClaw_MOST_comparisons/topo/PacificDEMs/*4min.tt3
"""

from __future__ import print_function

from pylab import *
from clawpack.geoclaw import topotools
from clawpack.clawutil.data import get_remote_file
import os

# Fetch earthquake source model (dtopo file):

url_geoclaw = 'http://depts.washington.edu/clawpack/geoclaw/'

url = os.path.join(url_geoclaw, 'dtopo/tohoku/2011Tohoku_deformation.asc')
get_remote_file(url, output_dir='.', verbose=True)


# Read etopo1 topography data from NCEI thredds server:

# Portion east of -180 (date line):

etopo1_url = 'https://www.ngdc.noaa.gov/thredds/dodsC/global/ETOPO1_Ice_g_gmt4.nc'
extent = [-180, -110, 20, 60]
print('Attempting to read etopo1 data from\n %s' % etopo1_url)
etopo = topotools.read_netcdf(path=etopo1_url, extent=extent,
                              coarsen=1, verbose=True)

fname = 'etopo1_-180_-110_20_60_1min.asc'
etopo.write(fname, topo_type=3)
print('Created ',fname)

# Portion west of 180 (date line):
extent = [120, 180, 20, 60]
print('Attempting to read etopo1 data from\n %s' % etopo1_url)
etopo = topotools.read_netcdf(path=etopo1_url, extent=extent,
                              coarsen=1, verbose=True)

# shift longitude to agree with coordinates of first topo file (longitude West):
etopo._x = etopo.x - 360.
etopo._X = etopo.X - 360.
etopo.generate_2d_coordinates()

fname = 'etopo1_-240_-180_20_60_1min.asc'
etopo.write(fname, topo_type=3)
print('Created ',fname)


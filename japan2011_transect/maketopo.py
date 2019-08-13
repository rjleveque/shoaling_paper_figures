
from __future__ import print_function

from pylab import *
from clawpack.geoclaw import topotools

# read in slice of etopo1 topography data:

etopo1_url = 'https://www.ngdc.noaa.gov/thredds/dodsC/global/ETOPO1_Ice_g_gmt4.nc'
extent = [-128, -124, 44, 44.5]
print('Attempting to read etopo1 data from\n %s' % etopo1_url)
etopo = topotools.read_netcdf(path=etopo1_url, extent=extent)

#topodir = '/Users/rjl/topo/westport_topo/'
#etopo.read(topodir+'etopo1_-132_-122_42_50_1min.asc',3)

# select a single slice at the desired latitude:
yslice = 44.2
je = find(etopo.y<yslice).max()
print('Extracting slice at latitude %.6f' % etopo.y[je])

xe = etopo.x
Be = etopo.Z[je,:]

if 0:
    je_shore = find(Be>0).min()
    xe_shore = xe[je_shore]

    xe_to_shore = xe[:je_shore]
    Be_to_shore = Be[:je_shore]

    d = vstack((xe_to_shore, Be_to_shore)).T

d = vstack((xe, Be)).T

fname = 'etopo1_transect.txt'
header = 'Transect of etopo1 data at latitude %.2f\n' % yslice
header += 'Columns:  longitude, B (topo relative to MSL)'
savetxt(fname, d, fmt='%.6f', header=header)
print('Created ',fname)


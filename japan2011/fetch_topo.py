"""
Fetch topo and dtopo files needed to run Tohoku event on 4-minute resolution
over the Pacific.
"""

from clawpack.clawutil.data import get_remote_file
import os

url_geoclaw = 'http://depts.washington.edu/clawpack/geoclaw/'

url = os.path.join(url_geoclaw, 'dtopo/tohoku/2011Tohoku_deformation.asc')
get_remote_file(url, output_dir='.', verbose=True)

url = os.path.join(url_geoclaw, 'topo/etopo/etopo1_-180_-60_-65_65_4min.tt3')
get_remote_file(url, output_dir='.', verbose=True)

url = os.path.join(url_geoclaw, 'topo/etopo/etopo1_-240_-180_-65_65_4min.tt3')
get_remote_file(url, output_dir='.', verbose=True)


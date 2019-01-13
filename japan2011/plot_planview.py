
from pylab import *
import os
import setplot
from clawpack.visclaw.frametools import plotframe
from clawpack.visclaw.plottools import plotbox

pd = setplot.setplot()
pd.outdir=os.path.abspath('_output')

savefig_ext = '.jpg'

def savefigp(fname):
    savefig(fname, bbox_inches='tight')
    print('Created %s' % fname)

    
frameno = 1
plotframe(frameno,pd)
figure(0)
#axis([-140,-122,40,50]) # set in setplot.py
plotbox([-128,-123.5,43,45],kwargs={'color':'k','linewidth':1.5})
fname = 'pacific_f%s' % str(frameno).zfill(4) + savefig_ext
savefigp(fname)

figure(1)
plot([-127,-124],[44.4,44.4],'k')
text(-126.9,44.45,'Transect A', fontsize=15, color='k')
plot([-127,-124],[44.2,44.2],'b')
text(-126.9,44.05,'Transect B', fontsize=15, color='b')
xticks(range(-128,-123),fontsize=15)
yticks(arange(43.2,45,0.4),fontsize=15)
xlabel('longitude',fontsize=15)
ylabel('latitude',fontsize=15)
fname = 'planview_f%s' % str(frameno).zfill(4) + savefig_ext
savefigp(fname)
    
frameno = 3
plotframe(frameno,pd)
figure(1)
plot([-127,-124],[44.4,44.4],'k')
text(-126.9,44.45,'Transect A', fontsize=15, color='k')
plot([-127,-124],[44.2,44.2],'b')
text(-126.9,44.05,'Transect B', fontsize=15, color='b')
xticks(range(-128,-123),fontsize=15)
yticks(arange(43.2,45,0.4),fontsize=13)
xlabel('longitude',fontsize=13)
ylabel('latitude',fontsize=13)
fname = 'planview_f%s' % str(frameno).zfill(4) + savefig_ext
savefigp(fname)


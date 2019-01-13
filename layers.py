
from __future__ import print_function
from pylab import *
import os

savefig_ext = '.jpg'
figdir = 'figures'
os.system('mkdir -p %s' % figdir)

def save_figure(fname):
    """Save figure to figdir with desired extension"""
    full_fname = os.path.join(figdir,fname) + savefig_ext
    savefig(full_fname, bbox_inches='tight')
    print('Created %s' % full_fname)

hl = 3200.
hr = 300.
g = 9.81
xr = 20e3
cl = sqrt(g*hl)
cr = sqrt(g*hr)

x0 = -100.
x1 = -40.
x2 = 0.
x3 = 40.
x4 = 100.
x = [x0, x1, x2, x3, x4]

h0 = hl
h1 = 1600.
h2 = 1000.
h3 = hr

c0 = cl
c1 = sqrt(g*h1)
c2 = sqrt(g*h2)
c3 = cr

tfinal = 5.
count = 0

def wave(t1,i,j,x,c):
    global count
    print('count = %i, t1 = %s, i = %i, j = %i' % (count,t1,i,j))
    if count > 5000:
        return
    count += 1
    if t1>tfinal:
        return
    k = min(i,j)
    t2 = t1 + abs((x[j]-x[i])/c[k])
    plot([x[i],x[j]], [t1,t2], 'b')
    if (j>0) and (j<len(c)):
        wave(t2,j,j+1,x,c)
        wave(t2,j,j-1,x,c)

def plot_axes(xin):
    for j in range(1,len(xin)-1):
        plot([xin[j],xin[j]], [0,tfinal], 'k')
    xlim(-110,110)
    ylim(0,tfinal)
    axis('off')

def plot_topo(x,h):
    #figure(10, figsize=(6,4))
    #clf()
    xtopo = [x[0]]
    htopo = [h[0],h[0]]
    for i in range(1, len(x)-1):
        xtopo.append(x[i]) 
        xtopo.append(x[i]) 
        htopo.append(h[i]) 
        htopo.append(h[i]) 
    xtopo.append(x[-1])
    xtopo = array(xtopo)
    htopo = array(htopo)
    ztopo = -htopo
    fill_between(xtopo, ztopo, color=[.7,.7,1])
    plot(xtopo,ztopo,'k')
    plot(xtopo,0*ztopo,'b')
    xlim(-110,110)
    ylim(-3300,100)
    xticks()
    yticks()
    axis('off')


figure(30, figsize=(4,8))
clf()
x = [x0,x2,x4]
c = [c0, c3]
h = [h0, h3]

axes([.1,.1,.9,.6])
plot_axes(x)
wave(0,0,1,x,c)

text(-20,-0.2,' $x \longrightarrow$', fontsize=20)
text(-110,3,'time $\longrightarrow$',rotation=90, fontsize=20)

axes([.1,.75,.9,.15])
plot_topo(x,h)

save_figure('topo_and_waves0')


figure(31, figsize=(4,8))
clf()
x = [x0,x1,x3,x4]
c = [c0, c1, c3]
h = [h0, h1, h3]

axes([.1,.1,.9,.6])
plot_axes(x)
wave(0,0,1,x,c)

text(-20,-0.2,' $x \longrightarrow$', fontsize=20)

axes([.1,.75,.9,.15])
plot_topo(x,h)

save_figure('topo_and_waves1')

figure(32, figsize=(4,8))
clf()
h0 = hl
h1 = 2000.
h2 = 1000.
h3 = hr

c0 = cl
c1 = sqrt(g*h1)
c2 = sqrt(g*h2)
c3 = cr

x = [x0,x1,x2,x3,x4]
c = [c0, c1, c2, c3]
h = [h0, h1, h2, h3]

axes([.1,.1,.9,.6])
plot_axes(x)
wave(0,0,1,x,c)

text(-20,-0.2,' $x \longrightarrow$', fontsize=20)

axes([.1,.75,.9,.15])
h = [h0,h1,h2,h3]
plot_topo(x,h)

save_figure('topo_and_waves2')

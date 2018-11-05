#! /usr/bin/env python

import sys
import os
import StringIO
#import numpy
from numpy import *
#import matplotlib as mpl
#matplotlib.use('Agg')
from matplotlib import pyplot, rc
from matplotlib.patches import Ellipse
from pylab import * # ORDER MUST BE MAINTAINED AS 1. matplotlib  AND 2.pylab

###
evalcmap  = matplotlib.cm.get_cmap('jet')
cNorm     = matplotlib.colors.Normalize(vmin=0, vmax=1)
scalarMap = matplotlib.cm.ScalarMappable(norm=cNorm, cmap='jet')
########################################################################
# read file
carg     = 1
Vector   = False
Dr = 0.001
dt = 0.00004
if(size(sys.argv)<2) :
    sys.stderr.write('Usage : i. dump_file ii. slice position iii. scale of vectors \n')

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-vec":
            Vector = True
            carg += 1

dumpf = sys.argv[carg]
carg += 1
zcut = int(sys.argv[carg])
carg += 1
sc = int(sys.argv[carg])
carg += 1
f = open(dumpf,'r')
count =0
#directly read from files
for line in f:  # a file in the same style with lammps dumpfile
    count+=1
    if count == 2:
        timestep= int(line)
    if count == 4:
        Natoms = int(line)
    if count == 6:
        num = line.split()
        L = float(num[1])
    if count == 9:
        x      = zeros(Natoms)
        y      = zeros(Natoms)
        z      = zeros(Natoms)
        dx     = zeros(Natoms)
        dy     = zeros(Natoms)
        dz     = zeros(Natoms)
        radius = zeros(Natoms)
    if count >=10:
        id = count - 10
        num= line.split()
        x[id]  = float(num[1])
        y[id]  = float(num[2])
        z[id]  = float(num[3])
        dx[id] = float(num[4])
        dy[id] = float(num[5])
        dz[id] = float(num[6])
        radius[id] = float(num[7])
# choose a slice that we want, from 3D to 2D, rescale the displacement
def slice(min):
    # axis is  z
    # min is the min limit, the width is always one particle diameter, 1
    max = min + 1
    xn    = []
    yn    = []
    dxn   = []
    dyn   = []
    radn  = []
    for i in range(Natoms):
        # in : new id
        if (z[i]> min and z[i] < max):
            r3 = sqrt(dx[i]*dx[i]+dy[i]*dy[i]+dz[i]*dz[i])
            r2 = sqrt(dx[i]*dx[i]+dy[i]*dy[i])
            xn.append(x[i])
            yn.append(y[i])
            if r2 == 0:
                dx[i]=0
                dy[i]=0
            else:
                dx[i] = dx[i]*r3/r2
                dy[i] = dy[i]*r3/r2
            dxn.append(dx[i])
            dyn.append(dy[i])
            radn.append(radius[i])
    return xn, yn, dxn, dyn, radn
#########################################################################
xn,yn,ex,ey,radn=slice(zcut)
d = zeros(len(ex))   # need to think how to colorcode, and how to plot the vectors

for i in range(len(xn)):
    d[i] = sqrt(ex[i]*ex[i] + ey[i]*ey[i])

Peeff = d /(timestep*dt*Dr)
# Peeff as colorcode referance

ells = [Ellipse(xy=(xn[i], yn[i]),
                width=2*radn[i], height=2*radn[i]) for i in range(len(xn))]

fig, ax = plt.subplots(subplot_kw={'aspect': 'equal'})
elli =0
for e in ells:
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    fcstr = 'r'
    ecstr = 'k'
    cval = (Peeff[elli]-Peeff.min())/(Peeff.max()-Peeff.min())
    if cval > 1:
        cval = 1
    if cval < 0:
        cval = 0
    fcstr = scalarMap.to_rgba(cval) #'g'
    ecstr = scalarMap.to_rgba(cval) #'g'
    e.set_facecolor(fcstr)
    e.set_edgecolor(ecstr)
    e.set_alpha(0.5) # 0.5
    e.set_zorder(0)
    elli += 1

    #e.set_alpha(np.random.rand())
    #e.set_facecolor(np.random.rand(3))

ax.set_xlim(0, L)
ax.set_ylim(0, L)

quiver(xn,yn,ex,ey,units='xy', scale=sc)

plt.savefig('Conf-Displace%d-slice%d.png'%(timestep,zcut))
close(1)
#plt.show()
"""
# prepare the plot
fig = figure(figsize=(L,L))  # define the plot size
### Figure:1 particle configuration
ax   = fig.add_axes([0.13, 0.28, 0.72, 0.]) #[0.13, 0.28, 0.72, 0.]
#fig, ax = plt.subplots()
#ells = [Ellipse(xy=(lop.x[i]%dL[0], lop.y[i]%dL[1]), width=2*lop.rad[i], height=2*lop.rad[i]) for i in range(0, len(lop.x))]
ells = [Ellipse(xy=(xn[i], yn[i]), width=2*radn[i], height=2*radn[i]) for i in range(0, len(xn))]  # why 0?

d = zeros(len(ex))   # need to think how to colorcode, and how to plot the vectors
for i in range(len(xn)):
    d[i] = sqrt(ex[i]*ex[i] + ey[i]*ey[i])
elli = 0
for e in ells:
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    fcstr = 'r'
    ecstr = 'k'

    if Vector:
        cval = (d[elli]-d.min())/(d.max()-d.min())
        if cval > 1:
            cval = 1
        if cval < 0:
            cval = 0
        fcstr = scalarMap.to_rgba(cval) #'g'
        ecstr = scalarMap.to_rgba(cval) #'g'

    e.set_facecolor(fcstr)
    e.set_edgecolor(ecstr)
    e.set_alpha(0.5) # 0.5
    e.set_zorder(0)
    elli += 1

if Vector:


###################################################################

# Figure:1 frame properties
margin = 0.6
ax.set_xlim(-margin, L+margin)
ax.set_ylim(-margin, L+margin)
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text', usetex=True)
xticks(fontsize=20)
yticks(fontsize=20)

#ax.axis('off')

#image = a.imshow(data, origin='lower', cmap=cm.jet,vmin=min,vmax=max)
#xticks(ticklist, ('0', '', '20', '', '40', '', '60', '', '80', '', '100', '', '120', '', '140', '', '160'))
#yticks(ticklist, ('0', '', '20', '', '40', '', '60', '', '80', '', '100', '', '120', '', '140', '', '160'))
#yticks(fontsize='large')

###################################################################

###################################################################

# colorbar:
cax = fig.add_axes([0.86, 0.28, 0.03, 0.7]) #[0.86, 0.28, 0.03, 0.7]
fc  = mpl.colorbar.ColorbarBase(cax, cmap='jet', orientation='vertical')
fc.set_ticks([(d.min()-d.min())/(d.max()-d.min()), 0.5*(d.max()-d.min())/(d.max()-d.min()), (d.max()-d.min())/(d.max()-d.min())])
#fc.ax.set_yticklabels([r'\textbf{'+str(minv)+'}', r'\textbf{'+str(0.5*(minv+maxv))+'}', r'\textbf{'+str(maxv)+'}'])
yticks(fontsize=20)
text(1.15, 0.9,'theta', rotation='vertical', fontsize=20)
"""
###################################################################

# Important for sheared memory

#! /usr/bin/env python

import sys
import os
import StringIO
#import numpy
from numpy import *
from lammpsOperations import *
#import matplotlib as mpl
#matplotlib.use('Agg')
from matplotlib import pyplot, rc
from matplotlib.patches import Ellipse
from pylab import * # ORDER MUST BE MAINTAINED AS 1. matplotlib  AND 2.pylab   

Lx       = 10.0
Ly       = 10.0
w        = 0.72
h        = w-0.02
first    = 0
dt       = 0.001
gdot     = 0.001
minv     = -1.0 
maxv     = 1.0
Velocity = False
carg     = 1

### for eigenvalue streamlines
evalcmap  = matplotlib.cm.get_cmap('jet')
cNorm     = matplotlib.colors.Normalize(vmin=0, vmax=1)
scalarMap = matplotlib.cm.ScalarMappable(norm=cNorm, cmap='jet')

###################################################################################
###################################################################################
if(size(sys.argv)<4) :
    sys.stderr.write('Usage : i. dump_file \n')
    sys.stderr.write('        ii. eigenvector_file\n')
    sys.stderr.write('        iii. snap number\n')
    exit()
    
for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-vel":
            Velocity = True
            carg += 1
        if word == "-set": # set colorbar boundary for the cg variable
            carg += 1
            minv = float(sys.argv[carg])
            carg += 1
            maxv = float(sys.argv[carg])
            carg += 1
            print "# min and max limit ", minv, maxv
        if word == "-dt": # set colorbar boundary for the cg variable
            carg += 1
            dt = float(sys.argv[carg])
            carg += 1
            print "# dt", dt

dumpf = sys.argv[carg]
carg += 1
eivf  = sys.argv[carg]
carg += 1
sid   = int(sys.argv[carg])
carg += 1
print dumpf, eivf, sid 
###################################################################################

###################################################################################

############################################
# read dump file
if not os.path.exists(dumpf):
    sys.stderr.write('dump file does not exist\n')
    exit()
    
lop     = LammpsOperations()
lop.readFile(dumpf, sid, True)
ts0     = lop.tsteps

############################################
ex = []
ey = []
th = []
for line in open(eivf):
    tmp = line.split()

for i in range(lop.nb_atoms):
    ex.append(float(tmp[i]))
for i in range(lop.nb_atoms,2*lop.nb_atoms):
    ey.append(float(tmp[i]))
for i in range(2*lop.nb_atoms,3*lop.nb_atoms):
    th.append(float(tmp[i]))
#####################################################################
fig = figure(figsize=(Lx,Ly))

###################################################################
### Figure:1 particle configuration
ax   = fig.add_axes([0.13, 0.28, w, h])
dL   = [lop.cell[1]-lop.cell[0], lop.cell[3]-lop.cell[2]]

"""
for i in range(0, len(lop.x)):
    lop.x[i] -= lop.cell[2]
    lop.y[i] -= lop.cell[2]
"""    
        
#ells = [Ellipse(xy=(lop.x[i]%dL[0], lop.y[i]%dL[1]), width=2*lop.rad[i], height=2*lop.rad[i]) for i in range(0, len(lop.x))]
ells = [Ellipse(xy=(lop.x[i], lop.y[i]), width=2*lop.rad[i], height=2*lop.rad[i]) for i in range(0, len(lop.x))]


if Velocity:
    print "# min and max theta ", min(th), max(th)


elli = 0
for e in ells:
    ax.add_artist(e)
    e.set_clip_box(ax.bbox)
    fcstr = 'r'
    ecstr = 'k'

    if Velocity:
        cval = (th[elli]-minv)/(maxv-minv)
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

if Velocity:
    quiver(lop.x,lop.y,ex,ey,scale=1)

###################################################################
# Figure:1 frame properties
margin = 0.6
#ax.set_xlim(-margin, dL[0]+margin)
ax.set_xlim(-margin, dL[1]+margin)
ax.set_ylim(-margin, dL[1]+margin)
#ax.set_xlim(-margin+lop.cell[0], lop.cell[1]+margin)
#ax.set_xlim(-margin+lop.cell[2], lop.cell[3]+margin)
#ax.set_ylim(-margin+lop.cell[2], lop.cell[3]+margin)

#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
#rc('text', usetex=True)
xticks(fontsize=20)
yticks(fontsize=20)

#ax.axis('off')
"""
image = a.imshow(data, origin='lower', cmap=cm.jet,vmin=min,vmax=max)
xticks(ticklist, ('0', '', '20', '', '40', '', '60', '', '80', '', '100', '', '120', '', '140', '', '160'))
yticks(ticklist, ('0', '', '20', '', '40', '', '60', '', '80', '', '100', '', '120', '', '140', '', '160'))
yticks(fontsize='large')
"""
###################################################################

###################################################################

# colorbar:
cax = fig.add_axes([0.86, 0.28, 0.03, h])
fc  = mpl.colorbar.ColorbarBase(cax, cmap='jet', orientation='vertical')
fc.set_ticks([(minv-minv)/(maxv-minv), 0.5*(maxv-minv)/(maxv-minv), (maxv-minv)/(maxv-minv)])
#fc.ax.set_yticklabels([r'\textbf{'+str(minv)+'}', r'\textbf{'+str(0.5*(minv+maxv))+'}', r'\textbf{'+str(maxv)+'}'])
yticks(fontsize=20)
text(1.15, 0.9,'theta', rotation='vertical', fontsize=20)

###################################################################
    
#fname = 'scfg-t-'+str(ts)+'.png'
#print 'Saving frame', fname
#savefig(fname)
show()
close(1) # Important for sheared memory
fig.clf()
    

#! /usr/bin/env python

import sys
import os
import StringIO
from pylab import *
from math import pi, atan2, sin, cos, sqrt, floor, exp
from matplotlib.patches import Ellipse
from atoms import *


shiftx = float(sys.argv[1])
shifty = float(sys.argv[2])
filename1 = sys.argv[3]
filename2 = sys.argv[4]

datafile1 = file(filename1,'rb')
datafile2 = file(filename2,'rb')

[cell1, data1, format1] = readFile(datafile1)
[cell2, data2, format2] = readFile(datafile2)
datafile1.close()
datafile2.close()

if cell1.L.any() != cell2.L.any() or size(data1,0) != size(data2,0):
    print "Error: files sizes do not match"
    sys.exit(0)

listnb = size(data1,0)
print "Found ", listnb, " list(s)"

fig = figure(figsize=(8,8))
ax  = fig.add_subplot(111, aspect='equal')

listnb = size(data1)

for l in range(0,listnb):
    N = size(data1[l].data)
    [X, Y, U, V] = computeDisplacementField_mdb(cell1, cell2, data1[l], data2[l], shiftx, shifty)

    D2 = [(U[i]*U[i] + V[i]*V[i])/0.3/0.3 for i in range(0,size(U))]
    R =  [float(data1[l].radius) for i in range(0, N)]

    print max(D2)

#   R =  [float(l.radius) for i in range(0, N)]
#   drawAtoms(ax, X, Y, R)
#drawAtomsMap(ax, X, Y, R)
    quiver(X,Y,U,V, units='dots')

margin = 8
ax.set_xlim(-margin, 1.5*cell1.L[0]+margin)
ax.set_ylim(-margin, cell1.L[1]+margin)

show()



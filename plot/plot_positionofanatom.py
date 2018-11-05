#! /usr/bin/env python

import sys
import os
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp
#from matplotlib import *
from atoms import *

def projectIntoBaseCell(X, Y):
    m = floor(Y/cell.L[1])
    Y -= m * cell.L[1]
    X -= m * cell.Dx
        
    m = floor(X/cell.L[0])
    X -= m * cell.L[0]
    #print [X, Y]
    return [float(X), float(Y)]
    

shift = [float(sys.argv[1]), float(sys.argv[2])]

first = 1
embed = 0
X = []
Y = []
X1 = []
Y1 = []

fig = figure(figsize=(8,8))
fig.subplots_adjust(0,0,1,1)
ax = fig.add_subplot(111)
#axis(ratio='exact')

for filename in sys.argv[3:]:
    
    print "Reading", filename
    datafile = file(filename,'rb')
    [cell, all, format] = readFile(datafile)
    datafile.close()
    
    if first == 1:
        first = 0
        D0 = cell.Dx

    dgamma = (cell.Dx-D0)/cell.L[1]
    dgamma = 0.2
    listnb = size(all)
    print "Found ", listnb, " list(s)"
    print "Format ", format

    id = 33
    nlist = -1
    # for listcount in range(size(all)):
    for listcount in range(1):
        list = all[listcount]
        nlist += 1
        N = size(list.data)
        print N, list.radius
        x = float(list.data[id][0]) 
        y = float(list.data[id][1]) 
        Y.append(y)
        X.append(x)


        a = projectIntoBaseCell(x,y)
        Y1.append(a[1])
        X1.append(a[0])

#ax.plot(X, Y, 'b', X1, Y1, 'r')
margin = 1.0
#ax.set_xlim(-margin-0.5*cell.L[0], 1.5*cell.L[0]+margin)
#ax.set_ylim(-margin-0.5*cell.L[1], 1.5*cell.L[1]+margin)

#axis('on')
    #fname = filename+'.png'
    #print 'Saving frame', fname
    #savefig(fname)
    #savefig("tmp.png")

show()
#file2 = open("Output",'w')
#print >> file2, "# X Y X0 Y0"
#for i in range(0, len(X)):
#    print >> file2, X[i], Y[i], X1[i], Y1[i]

#file2.close() 



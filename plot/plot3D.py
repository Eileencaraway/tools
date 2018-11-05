#! /usr/bin/env python

import sys
import os
import StringIO
from math import pi, atan2, sin, cos, sqrt, floor, exp
from matplotlib import *
from mpl_toolkits.mplot3d import Axes3D
from atoms3D import *

small   = True
large   = True
image   = True
verbose = False
first   = 1
embed   = 0
shift = [0.0, 0.0, 0.0]
carg    = 1
if len(sys.argv)<2:
    sys.stderr.write("Usage: filename(s) ")
    print
    sys.exit()

for word in sys.argv[1:]:
    if word[0] == "-":
        if word == "-v":
            verbose = True
            carg += 1

        if word == "-s":
            carg += 1
            for i in range(3):
                shift[i] = [float(sys.argv[carg])]
                carg += 1
            print shift

        if word == "-large":
            small = False
            carg += 1

        if word == "-small":
            large = False
            carg += 1


for filename in sys.argv[carg:]:

    print "Reading", filename
    datafile = file(filename,'rb')
    [cell, all, format] = readFile(datafile)
    datafile.close()

    if first == 1:
        first = 0
        D0 = cell.Dx

    listnb = size(all)
    print "Found ", listnb, " list(s)"
    print "Format ", format


    fig = figure()
    ax = Axes3D(fig)
    #axis(ratio='exact')

    nlist = -1
    for listcount in range(size(all)):
        list = all[listcount]
        nlist += 1
        N = size(list.data)
        print N, list.radius

        Z =  [float(list.data[i][2]+shift[2]) for i in range(0, N)]
        Y =  [float(list.data[i][1]+shift[1]) for i in range(0, N)]
        X =  [float(list.data[i][0]+shift[0]) for i in range(0, N)]
        R =  [float(list.radius) for i in range(0, N)]
        #cell.projectIntoBaseCell(X,Y,Z)

        index = 3
        if format & OUTPUT_VELOCITIES:
            U =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            V =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            W =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1

            print "vels : ", min(U), max(U), min(V), max(V), min(W), max(W)

            if (image and listcount > 1):
                ax.scatter(X, Y, Z, c='k', marker='o')
            if (large and listcount == 0):
                ax.scatter(X, Y, Z, c='r', marker='o')
            if (small and listcount == 1):
                ax.scatter(X, Y, Z, c='g', marker='o')


        else:
            if (image and nlist > 1):
                ax.scatter(X, Y, Z, c='k', marker='o')
            if (large and nlist == 0):
                ax.scatter(X, Y, Z, c='r', marker='o')
            if (small and nlist == 1):
                ax.scatter(X, Y, Z, c='g', marker='o')



        if format & OUTPUT_FORCES:
            FX =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            FY =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            FZ =  [float(list.data[i][index]) for i in range(0, N)]
            index += 1
            print min(FX), max(FX), min(FY), max(FY), min(FZ), max(FZ)
            #quiver(X,Y,FX,FY, color='r')

        #margin = 1.0
        #ax.set_xlim(-margin-0.5*cell.L[0], 1.5*cell.L[0]+margin)
        #ax.set_ylim(-margin-0.5*cell.L[1], 1.5*cell.L[1]+margin)
        #ax.set_zlim3D(-margin-0.5*cell.L[2], 1.5*cell.L[2]+margin)

#axis('off')

if verbose:
    if (small and large):
            fname = filename+'.png'
            print 'Saving frame', fname
            savefig(fname)
    else:
        if large:
            fname = filename+'-large.png'
            print 'Saving frame', fname
            savefig(fname)
        if small:
            fname = filename+'-small.png'
            print 'Saving frame', fname
            savefig(fname)

else:
    show()

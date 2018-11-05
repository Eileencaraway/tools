#! /usr/bin/env python

import sys
import os
import StringIO
import numpy as np
from lammpsOperations import *
#pathdir = os.environ['HOME']+'/mols/misc_scripts'
#sys.path.append(pathdir)


###################################################################################
dt     = 1
verbose=False
COM    =False
###################################################################################

###################################################################################
if(size(sys.argv)<3):
    sys.stderr.write('Usage : i.   dump_file \n')
    sys.stderr.write('        ii.  column ids\n')
    exit()

carg = 1
for word in sys.argv[carg:]:
    if word[0] == "-":
        if word == "-v": # set colorbar boundary for the cg variable
            verbose = True
            carg += 1
        if word == "-dt":
            carg += 1
            dt = float(sys.argv[carg])
            carg += 1
        if word == "-com":
            carg += 1
            COM   = True

dumpf = sys.argv[carg]
carg += 1
colist=[]
while carg<size(sys.argv):
    colist.append(int(sys.argv[carg]))
    carg += 1

nbCols=len(colist) # number of columns
if verbose:
    print "# ", dumpf, nbCols, colist
###################################################################################

############################################
# select snap ids corresponding to timesteps
if not os.path.exists(dumpf):
    sys.stderr.write(dumpf+' does not exist\n')
    exit()

lop     = LammpsOperations()
lop.readSelectedColumns(dumpf, 0, colist, verbose)
ts0     = lop.tsteps
cols    = lop.columns
com0    = np.zeros(nbCols)
if COM:
    for c in range(nbCols):
        com0[c] = mean(cols[c])

#print cols[0][11], cols[1][11]
#print cols[0][104], cols[1][104]

ts1 = 1
sid = 1
while ts1 > 0:
    lop     = LammpsOperations()
    lop.readSelectedColumns(dumpf, sid, colist, verbose)
    ts1     = lop.tsteps
    dts     = ts1-ts0
    sid    += 1

    if ts1==0:
        break

    dcols   = lop.columns-cols

    if COM:
        com1    = np.zeros(nbCols)
        for c in range(nbCols):
            com1[c] = mean(lop.columns[c])

        for c in range(nbCols):
            for i in range(lop.nb_atoms):
                dcols[c][i] -= (com1[c]-com0[c])

    dr2     = 0
    for c in range(nbCols):
        dr2 += mean(dcols[c]*dcols[c])

    print dts*dt, dr2
############################################

#! /usr/bin/env python

import sys
import os
import StringIO
import numpy as np
from lammpsOperationsnp import *
from scipy import *
import glob
#pathdir = os.environ['HOME']+'/mols/misc_scripts'
#sys.path.append(pathdir)


###################################################################################
dt     = 1
verbose=False
COM    =False
###################################################################################

###################################################################################
if(size(sys.argv)<3):
    sys.stderr.write('Usage : i.  column ids\n')
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
# This part is for sort and read the files in order
List=[]
for filename in glob.glob('dumpfile.*'):
    #print filename
    List.append(filename)
List.sort()
################################################################################
f0 = open('cluster_id.dat','r')
clusterid =[]
for line in f0:
    clusterid.append(int(line))
nid = len(clusterid)
#################################################################################
# select snap ids corresponding to timesteps
lop     = LammpsOperations()
lop.readSelectedColumns(List[0], colist, verbose)
ts0     = lop.tsteps
cols    = lop.columns
com0    = np.zeros(nbCols)
if COM:
    for c in range(nbCols):
        com0[c] = mean(cols[c])


for j in range(1,len(List)):
    if not os.path.exists(List[j]):
        sys.stderr.write(List[j]+' does not exist\n')
        exit()

    lop     = LammpsOperations()
    lop.readSelectedColumns(List[j],colist, verbose)
    ts1     = lop.tsteps
    dts     = ts1-ts0

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

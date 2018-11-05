#! /usr/bin/env python

import sys
import os
import StringIO
from numpy import *
from lammpsOperations import *
pathdir = os.environ['HOME']+'/mols/misc_scripts'
sys.path.append(pathdir) 


###################################################################################
dt     = 0.001
gdot   = 0.001
verbose=False
###################################################################################

###################################################################################
if(size(sys.argv)<5) :
    sys.stderr.write('Usage : i.   dump_file \n')
    sys.stderr.write('        ii.  starting timestep\n')
    sys.stderr.write('        iii. ending timestep\n')
    sys.stderr.write('        iv.  timestep intervals\n')
    sys.stderr.write('        v.   atom id\n')
    print 
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

dumpf = sys.argv[carg]
carg += 1
tsrt  = float(sys.argv[carg])
carg += 1
tend  = float(sys.argv[carg])
carg += 1
ivals = float(sys.argv[carg])
carg += 1
aid   = int(sys.argv[carg])
carg += 1
###################################################################################

############################################
# select snap ids corresponding to timesteps
if os.path.exists(dumpf):
    lop     = LammpsOperations()
    lop.readFile(dumpf, 0, verbose)
    ts0     = lop.tsteps
    
    lop     = LammpsOperations()
    lop.readFile(dumpf, 1, verbose)
    ts1     = lop.tsteps
    dts     = ts1-ts0
    sds     = int((tsrt-ts0)/dts)
    sde     = int((tend-ts0)/dts)
    svals   = int(ivals/dts)
    sids    = arange(sds,sde,svals)
    tsvals  = arange(tsrt,tend,ivals)
else:
    print dumpf, " does not exist."

snapids = dict(zip(tsvals, sids))
############################################

############################################
print "# tsteps and positions of atom id ", aid
for ts in tsvals: 
    lop     = LammpsOperations()
    lop.readFile(dumpf, snapids[ts], verbose)
    print lop.tsteps, "  ", lop.x[aid], "   ", lop.y[aid], "   ", lop.ix[aid], "   ", lop.iy[aid], "   ", lop.cell[0], "  ", lop.cell[1], "  ", lop.vx[aid], "   ", lop.vy[aid]

    """
    print lop.tsteps, "  ", lop.x[aid], "   ", lop.y[aid], "   ", lop.cell[0], "  ", lop.cell[1], lop.cell[2], "  ", lop.cell[3],

    gamma  = lop.tsteps*dt*gdot
    gamma -= floor(gamma)
    dL   = [lop.cell[1]-lop.cell[0], lop.cell[3]-lop.cell[2]]

    if lop.x[aid] < lop.cell[2]:
        lop.x[aid] += dL[1]
    if lop.x[aid] >= lop.cell[3]:
        lop.x[aid] -= dL[1]

    print lop.x[aid]
    """
    

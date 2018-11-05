#! /usr/bin/env python
#non_gaussian parameter is a quantity of every datas to see whether the distribution is a gaussian or not
import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
import glob
###################################################################################
dt     = 0.00004
gdot   = 0.001
dim    = 3
verbose= False
###################################################################################
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
        if word == "-dim":
            carg += 1
            dim = int(sys.argv[carg])
            carg += 1

##############################################################################
f=open('msad.txt','w')
time=0
###############################################################################
# This part is for sort and read the files in order
List=[]
for filename in glob.glob('dumpfile.*'):
    #print filename
    List.append(filename)
List.sort()
##############################################################################
#This part is actually for initialize num_particle and some arrays
if os.path.exists(List[0]):
    if dim==3:
        lstr  = LammpsOperations()
        lstr.readFile3d(List[0], verbose)
    else:
        lstr  = LammpsOperations()
        lstr.readFile(List[0], verbose)
    L            = lstr.cell[1]
    num_particle = lstr.nb_atoms
    time0         = lstr.tsteps
else:
    print tsrt, " does not exist."

ax0=zeros(num_particle)
ay0=zeros(num_particle)
az0=zeros(num_particle)

ax1=zeros(num_particle)
ay1=zeros(num_particle)
az1=zeros(num_particle)

# initial angular displacement, because in the code
# there are equilibrium process, thus initial angular displacement is not zero
for i in range(num_particle):
    ax0[i]=lstr.thtx[i]
    ay0[i]=lstr.thty[i]
    if dim==3:
        az0[i]=lstr.thtz[i]
##############################################################################

for i in range(1,len(List)):
    tend=List[i]
    print tend
    # select snap ids corresponding to timesteps
    if os.path.exists(tend):
        if dim==3:
            lend  = LammpsOperations()
            lend.readFile3d(tend, verbose)
        else:
            lend  = LammpsOperations()
            lend.readFile(tend, verbose)
        time1    = lend.tsteps

    else:
        print tsrt, " does not exist."


#    for i in range(num_particle):
#        ax[i]=lend.omegax[i]
#        ay[i]=lend.omegay[i]
#        if dim==3:
#            az[i]=lend.omegaz[i]
 # angular displacement should be add up
 # and minus the overall value
    for i in range(num_particle):
        ax1[i]=lend.thtx[i]
        ay1[i]=lend.thty[i]
        if dim==3:
            az1[i]=lend.thtz[i]
    avgax = mean(ax1)
    avgay = mean(ay1)
    avgaz = mean(az1)

    ax1=ax1-avgax
    ay1=ay1-avgay
    az1=az1-avgaz

    ax1=ax1-ax0
    ay1=ay1-ay0
    az1=az1-az0

    masd=sqrt(mean(ax1**2)+mean(ay1**2)+mean(az1**2))
    msdstr=str(time1*dt)+' '+str(masd)+'\n'
    f.write(msdstr)

f.close()

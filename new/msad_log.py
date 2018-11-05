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
dt     = 1.0
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

f1=open('angular-displacement-dumpfile.txt','w')
f2=open('msad.txt','w')
f1.write("ID adx ady adz\n")
time=0
###############################################################################
# This part is for sort and read the files in order
f3=open('filename.txt','w')
List=[]
for filename in glob.glob('dumpfile.*'):
    #print filename
    List.append(filename)
List.sort()
for i in range(len(List)):
    startfile=List[i]
    #print startfile
    f3.write(startfile+'\n')
f3.close()
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
ax=zeros(num_particle)
ay=zeros(num_particle)
az=zeros(num_particle)
adx=zeros(num_particle)
ady=zeros(num_particle)
adz=zeros(num_particle)
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

    ax=zeros(num_particle)
    ay=zeros(num_particle)
    az=zeros(num_particle)

#    for i in range(num_particle):
#        ax[i]=lend.omegax[i]
#        ay[i]=lend.omegay[i]
#        if dim==3:
#            az[i]=lend.omegaz[i]

    for i in range(num_particle):
        ax[i]=lend.ADx[i]
        ay[i]=lend.ADy[i]
        if dim==3:
            az[i]=lend.ADz[i]

    avx=ax
    avy=ay
    avz=az

    gap= time1-time0
    adx+=avx*dt
    ady+=avy*dt
    adz+=avz*dt
    f1.write("TIMESTEP: %d TIME: %f \n"%(time1,time1*dt))
    for i in range(num_particle):
        f1.write("%d %f %f %f\n"%(i,adx[i],ady[i],adz[i]))
    masd=sqrt(mean(adx**2)+mean(ady**2)+mean(adz**2))
    msdstr=str(time1*dt)+' '+str(masd)+'\n'
    f2.write(msdstr)

    time0 = time1


f1.close()
f2.close()

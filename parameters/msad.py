#! /usr/bin/env python
#non_gaussian parameter is a quantity of every datas to see whether the distribution is a gaussian or not

import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *

###################################################################################
dt     = 0.000444288
gdot   = 0.001
dim    = 3
verbose= False
###################################################################################
if(size(sys.argv)<3) :
    sys.stderr.write('Usage : i.    starting time\n')
    sys.stderr.write('        ii.   ending time\n')
    sys.stderr.write('        iii.  timesteps\n')
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
        if word == "-dim":
            carg += 1
            dim = int(sys.argv[carg])
            carg += 1

start = int(sys.argv[carg])
carg += 1
end  = int(sys.argv[carg])
carg += 1
timesteps =  int(sys.argv[carg])
carg += 1
##############################################################################
total_file=end-start
masd=zeros(total_file)
f1=open('angular-displacement-dumpfile2.txt','w')
f2=open('masd2.txt','w')
f1.write("ID adx ady adz\n")
time=0

startfile='dumpfile.'+str(0).zfill(10)+'.txt'
if os.path.exists(startfile):
    if dim==3:
        lstr  = LammpsOperations()
        lstr.readFile3d(startfile, verbose)
    else:
        lstr  = LammpsOperations()
        lstr.readFile(startfile, verbose)
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


for k in range(total_file):
    tend='dumpfile.'+str(int(k+start)).zfill(10)+'.txt'
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
        ax[i]=lend.omegax[i]
        ay[i]=lend.omegay[i]
        if dim==3:
            az[i]=lend.omegaz[i]

    avx=ax
    avy=ay
    avz=az
    #print filename

    gap= time1-time0
    if gap == timesteps:
        adx+=avx*timesteps*dt
        ady+=avy*timesteps*dt
        adz+=avz*timesteps*dt
        f1.write("TIMESTEP: %d TIME: %f \n"%(time1,time1*dt))
        for i in range(num_particle):
            f1.write("%d %f %f %f\n"%(i,adx[i],ady[i],adz[i]))
        masd=mean(adx**2)+mean(ady**2)+mean(adz**2)
        msdstr=str(time1*dt)+' '+str(masd)+'\n'
        f2.write(msdstr)
    else:
        "TIMESTEP is not equal"
    time0 = time1


f1.close()
f2.close()

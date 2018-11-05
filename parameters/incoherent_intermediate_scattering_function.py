#! /usr/bin/env python

import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
#import matplotlib.pyplot as plt

pathdir = os.environ['HOME']+'/mols/misc_scripts'
sys.path.append(pathdir)


###################################################################################
dt     = 0.00099346
gdot   = 0.001
#k      = 10
dim    = 3
verbose= False
# ##################################################################################

###################################################################################
if(size(sys.argv)<5) :
    sys.stderr.write('Usage : i.    initial time\n')
    sys.stderr.write('        ii.   interval steps \n')
    sys.stderr.write('        iii.  end time\n')
    sys.stderr.write('        iv.   k value\n')
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
        if word == "-q":
            carg += 1
            dim = float(sys.argv[carg])
            carg += 1

tsrt = int(sys.argv[carg])
carg += 1
ivals  = int(sys.argv[carg])
carg += 1
tend  = int(sys.argv[carg])
carg += 1
k     = int(sys.argv[carg])
carg += 1
###################################################################################

def fun(dsrt,dend):
    # select snap ids corresponding to timesteps
    if os.path.exists(dsrt)&os.path.exists(dend):
        if dim==3:
            lstr  = LammpsOperations()
            lstr.readFile3d(dsrt, verbose)
            lend  = LammpsOperations()
            lend.readFile3d(dend, verbose)
        else:
            lstr  = LammpsOperations()
            lstr.readFile(dsrt, verbose)
            lend  = LammpsOperations()
            lend.readFile(dend, verbose)

        ts0     = lstr.tsteps
        ts1     = lend.tsteps
        dts     = ts1-ts0
        L       = lstr.cell[1]
        num_particle =lstr.nb_atoms
    else:
        print tsrt, " does not exist. or", tend, " does not exist. "



    ###################################################################################


    dx=zeros(num_particle)
    dy=zeros(num_particle)
    dz=zeros(num_particle)
    Fs=zeros(num_particle)
    for i in range(num_particle):
        dx[i]=lend.xu[i]-lstr.xu[i]
        dy[i]=lend.yu[i]-lstr.yu[i]
        if dim==3:
            dz[i]=lend.zu[i]-lstr.zu[i]
    avgx=mean(dx)
    avgy=mean(dy)
    avgz=mean(dz)

    for i in range(num_particle):
        dx[i]-=avgx
        dy[i]-=avgy
        if dim==3:
            dz[i]-=avgz
            Fs[i]=(cos(k*dx[i])+cos(k*dy[i])+cos(k*dz[i]))/3
        else:
            Fs[i]=(cos(k*dx[i])+cos(k*dy[i]))/2


    Fs_avg=mean(Fs)

    return Fs_avg,dts

###################################################################################
# for this function the input is a list of dumpfile, so the input should be a starting filename, intervals and the ending time
#thus here I want to construct the string of the tend filename
total_file=(tend-tsrt)/ivals
print total_file
#t=arange(tsrt,tend,ivals)

Fs_value=zeros(total_file)
t=zeros(total_file)


dsrt= 'dumpfile.'+str(tsrt).zfill(10)+'.txt'
f=open('ISF-k%d.txt'%k,'w')

for i in range(total_file):
    step=tsrt+i*ivals
    #print '%s%s%s'%('dumpfile.',tt.zfill(10),'.txt')
    #print 'dumpfile.'+tt.zfill(10)+'.txt'

    dend='dumpfile.'+str(step).zfill(10)+'.txt'
    Fs_value[i],t[i]=fun(dsrt,dend)
    f.write('%f %f\n'%(t[i],Fs_value[i]))

f.close()
'''
def plot_func():
    plt.plot(t,Fs_value)
    plt.xlabel("timesteps")
    plt.ylabel("Fs")
    plt.savefig("ISF-k%d.png"%k)

plot_func()
'''

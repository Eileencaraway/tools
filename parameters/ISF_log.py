#! /usr/bin/env python

import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
#import matplotlib.pyplot as plt

#pathdir = os.environ['HOME']+'/mols/misc_scripts'
#sys.path.append(pathdir)


###################################################################################
gdot   = 0.001
k      = 7
dim    = 3
verbose= False
# ##################################################################################

###################################################################################
if(size(sys.argv)<3) :
    sys.stderr.write('        i.   scale \n')
    sys.stderr.write('        ii. dt_integration \n')
    print
    exit()

carg = 1
for word in sys.argv[carg:]:
    if word[0] == "-":
        if word == "-v": # set colorbar boundary for the cg variable
            verbose = True
            carg += 1
        if word == "-dim":
            carg += 1
            dim = int(sys.argv[carg])
            carg += 1
        if word == "-q":
            carg += 1
            dim = float(sys.argv[carg])
            carg += 1

scale = int(sys.argv[carg])
carg += 1
dt   = float(sys.argv[carg])
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
        print dsrt, " does not exist. or", dend, " does not exist. "



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
total_file=scale*9
Fs_value=zeros(total_file)
t=zeros(total_file)
step=zeros(total_file)
tsrt = 0
dsrt= 'dumpfile.'+str(tsrt).zfill(10)+'.txt'
f=open('ISF.txt','w')
count=0
for j in range(scale):
    for i in range(1,10):
        step[count]=i*10**j
        count+=1


for files in range(total_file):
    dend='dumpfile.'+str(int(step[files])).zfill(10)+'.txt'
    print dend
    Fs_value[files],t[files]=fun(dsrt,dend)
    t[files]=t[files]*dt
    f.write('%f %f\n'%(t[files],Fs_value[files]))

f.close()

'''
def plot_func():
    plt.plot(t,Fs_value)
    plt.xlabel("timestep")
    plt.ylabel("Fs")
    plt.savefig("ISF.png")

plot_func()
'''

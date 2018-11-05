#! /usr/bin/env python
#non_gaussian parameter is a quantity of every datas to see whether the distribution is a gaussian or not

import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
#import matplotlib.pyplot as plt

pathdir = os.environ['HOME']+'/Dropbox/Code/tools/old/'
sys.path.append(pathdir)


###################################################################################
dt     = 0.000444288
gdot   = 0.001
dim    = 3
verbose= False
num_particle=10
# ##################################################################################

def onefile(tsrt):
    # select snap ids corresponding to timesteps
    if os.path.exists(tsrt):
        if dim==3:
            lstr  = LammpsOperations()
            lstr.readFile3d(tsrt, verbose)
        else:
            lstr  = LammpsOperations()
            lstr.readFile(tsrt, verbose)

        ts0     = lstr.tsteps
        L       = lstr.cell[1]
    else:
        print tsrt, " does not exist. or"

    omegax=zeros(num_particle)
    omegay=zeros(num_particle)
    omegaz=zeros(num_particle)

    for i in range(num_particle):
        omegax[i]=lstr.omegax[i]
        omegay[i]=lstr.omegay[i]
        if dim==3:
            omegaz[i]=lstr.omegaz[i]
    cx=mean(omegax)
    cy=mean(omegay)
    cz=mean(omegaz)

    for i in range(num_particle):
        omegax[i]=lstr.omegax[i]-cx
        omegay[i]=lstr.omegay[i]-cy
        if dim==3:
            omegaz[i]=lstr.omegaz[i]-cz



    return ts0,omegax,omegay,omegaz
###################################################################################
if(size(sys.argv)<1) :
    sys.stderr.write('Usage : i.    num_consider \n')
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

num_particle = int(sys.argv[carg])
carg += 1


###################################################################################
total_file=100000
'''
scale=8
total_file=scale*9

step=zeros(total_file)
count=0

for j in range(scale):
    for i in range(1,10):
        number=i*10**j
        step[count]=number
        count+=1
'''
thetax=zeros((total_file,num_particle))
thetay=zeros((total_file,num_particle))
thetaz=zeros((total_file,num_particle))
t=zeros(total_file)
##f1=open('trajectory.txt','w')
ox=zeros(num_particle)
oy=zeros(num_particle)
oz=zeros(num_particle)


dsrt='dumpfile.'+str(int(0)).zfill(10)+'.txt'
t[0],thetax[0],thetay[0],thetaz[0]=onefile(dsrt)

for k in range(1,total_file):
    dsrt='dumpfile.'+str(int(k)).zfill(10)+'.txt'
    t[k],ox,oy,oz=onefile(dsrt)
    thetax[k]=thetax[k-1]+ox
    thetay[k]=thetay[k-1]+oy
    thetaz[k]=thetaz[k-1]+oz

for i in range(num_particle):
    f1=open('theta-trajectory-%d.txt'%i,'w')
    for k in range(total_file):
        f1.write('%d %f %f %f\n'%(t[k],thetax[k][i],thetay[k][i],thetaz[k][i]))
    f1.close()

#####################################################################################
#def plot(x,y,x_name,y_name,title,filename):
#    plt.loglog(x,y)
#    plt.xlabel(x_name)
#    plt.ylabel(y_name)
#    plt.title(title)
#    plt.savefig(filename)

#plot(t,msd,'time','msd','msd plot','msd.png')

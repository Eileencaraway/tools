#! /usr/bin/env python
#non_gaussian parameter is a quantity of every datas to see whether the distribution is a gaussian or not

import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
import matplotlib.pyplot as plt

pathdir = os.environ['HOME']+'/Dropbox/Code/tools/'
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

    nx=zeros(num_particle)
    ny=zeros(num_particle)
    nz=zeros(num_particle)

    for i in range(num_particle):
        nx[i]=lstr.xu[i]
        ny[i]=lstr.yu[i]
        if dim==3:
            nz[i]=lstr.zu[i]
    cx=mean(nx)
    cy=mean(ny)
    cz=mean(nz)

    for i in range(num_particle):
        nx[i]=lstr.xu[i]-cx
        ny[i]=lstr.yu[i]-cy
        if dim==3:
            nz[i]=lstr.zu[i]-cz



    return ts0,nx,ny,nz
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
mx=zeros((total_file,num_particle))
my=zeros((total_file,num_particle))
mz=zeros((total_file,num_particle))
t=zeros(total_file)
##f1=open('trajectory.txt','w')

for k in range(total_file):
    dsrt='dumpfile.'+str(int(k)).zfill(10)+'.txt'
    t[k],mx[k],my[k],mz[k]=onefile(dsrt)

for i in range(num_particle):
    f1=open('trajectory-xu-%d.txt'%i,'w')
    for k in range(total_file):
        f1.write('%d %f %f %f\n'%(t[k],mx[k][i],my[k][i],mz[k][i]))
    f1.close()

#####################################################################################
def plot(x,y,x_name,y_name,title,filename):
    plt.loglog(x,y)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(title)
    plt.savefig(filename)

#plot(t,msd,'time','msd','msd plot','msd.png')

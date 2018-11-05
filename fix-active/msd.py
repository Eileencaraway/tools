#! /usr/bin/env python
#non_gaussian parameter is a quantity of every datas to see whether the distribution is a gaussian or not

import sys
import os
import glob
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
#import matplotlib.pyplot as plt

pathdir = os.environ['HOME']+'/mols/misc_scripts'
sys.path.append(pathdir)


###################################################################################
dt     = 0.00004
gdot   = 0.001
dim    = 3
verbose= False
# ##################################################################################

def onefile(tsrt,tend):

    # select snap ids corresponding to timesteps
    if os.path.exists(tsrt)&os.path.exists(tend):
        if dim==3:
            lstr  = LammpsOperations()
            lstr.readFile3d(tsrt, verbose)
            lend  = LammpsOperations()
            lend.readFile3d(tend, verbose)
        else:
            lstr  = LammpsOperations()
            lstr.readFile(tsrt, verbose)
            lend  = LammpsOperations()
            lend.readFile(tend, verbose)

        ts0     = lstr.tsteps
        ts1     = lend.tsteps
        dts     = ts1-ts0
        L       = lstr.cell[1]
        num_particle =lstr.nb_atoms
    else:
        print tsrt, " does not exist. or", tend, " does not exist. "

    dxu=zeros(num_particle)
    dyu=zeros(num_particle)
    dzu=zeros(num_particle)
    dru=zeros(num_particle)


    ave_dxu=0.0
    ave_dyu=0.0
    ave_dzu=0.0
    dxu_sum=0
    dyu_sum=0
    dzu_sum=0

    for i in range(num_particle):
        dxu[i]=lstr.xu[i]-lend.xu[i]
        dyu[i]=lstr.yu[i]-lend.yu[i]
        if dim==3:
            dzu[i]=lstr.zu[i]-lend.zu[i]

    avgx=mean(dxu)
    avgy=mean(dyu)
    avgz=mean(dzu)

    for i in range(num_particle):
        dxu[i]-= avgx
        dyu[i]-= avgy
        if dim == 3:
            dzu[i]-=avgz
            dru[i]=sqrt(dxu[i]**2+dyu[i]**2+dzu[i]**2)
        else:
            dru[i]=sqrt(dxu[i]**2+dyu[i]**2)

    msd=mean(dxu**2)+mean(dyu**2)+mean(dzu**2)

    return msd,dts
###################################################################################
'''
if(size(sys.argv)<3) :
    sys.stderr.write('Usage : i.    starting time\n')
    sys.stderr.write('        ii.   ending timescale\n')
    sys.stderr.write('        iii.  dt\n')
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

tsrt = int(sys.argv[carg])
carg += 1
scale  = int(sys.argv[carg])
carg += 1
dt  = float(sys.argv[carg])
carg += 1
'''
###################################################################################
'''
total_file=scale*9-tsrt
msd=zeros(total_file)
t=zeros(total_file)

step=zeros(total_file)

dsrt= 'dumpfile.'+str(tsrt).zfill(10)+'.txt'
print dsrt

f=open('msd.txt','w')
count=0
for j in range(1,scale):
    for i in range(1,10):
         number=i*10**j
         if number > tsrt:
             step[count]=number
             count+=1
'''
############################################################################
filename= []
## change to better way of listing the file name 
for infile in sorted(glob.glob('dumpfile.*.txt')):
    print infile 
    filename.append(infile)

dsrt=filename[0]
msd=zeros(len(filename))
t= zeros(len(filename))
f= open('msd.txt','w')
for k in range(1,len(filename)):
    #dend='dumpfile.'+str(int(step[k])).zfill(10)+'.txt'
    #print dend
    dend = filename[k]
    msd[k],t[k]=onefile(dsrt,dend)
    t[k]=t[k]*dt
    msdstr=str(t[k])+' '+str(msd[k])+'\n'
    f.write(msdstr)

f.close()
#####################################################################################
'''def plot(x,y,x_name,y_name,title,filename):
    plt.loglog(x,y)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(title)
    plt.savefig(filename)
'''
#plot(t,msd,'time','msd','msd plot','msd.png')

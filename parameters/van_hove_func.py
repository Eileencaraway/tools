#! /usr/bin/env python

import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
import matplotlib.pyplot as plt

pathdir = os.environ['HOME']+'/mols/misc_scripts'
sys.path.append(pathdir)


###################################################################################
dt     = 0.000444288
gdot   = 0.001
dim    = 3
verbose= False
# ##################################################################################

###################################################################################
if(size(sys.argv)<2) :
    sys.stderr.write('Usage : i.    starting dump_file\n')
    sys.stderr.write('        ii.   ending dump_file\n')
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

tsrt = sys.argv[carg]
carg += 1
tend  = sys.argv[carg]
carg += 1

###################################################################################

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



###################################################################################

dxu=zeros(num_particle)
dyu=zeros(num_particle)
dzu=zeros(num_particle)
dru=zeros(num_particle)
logdr=zeros(num_particle)


ave_dxu=0.0
ave_dyu=0.0
ave_dzu=0.0
dxu_sum=0
dyu_sum=0
dzu_sum=0

for i in range(num_particle):
    dxu[i]=lstr.xu[i]-lend.xu[i]
    dyu[i]=lstr.yu[i]-lend.yu[i]
    dxu_sum+=dxu[i]
    dyu_sum+=dyu[i]
    if dim==3:
        dzu[i]=lstr.zu[i]-lend.zu[i]
        dzu_sum+=dzu[i]



ave_dxu= dxu_sum/num_particle
ave_dyu= dyu_sum/num_particle
if dim==3:
    ave_dzu= dzu_sum/num_particle

print "ave of dx ",ave_dxu
print "ave of dy", ave_dyu

if dim==3:
    print "ave of dz", ave_dzu

for i in range(num_particle):
    dxu[i]-=ave_dxu
    dyu[i]-=ave_dyu
    if dim==3:
        dzu[i]-=ave_dzu
        dru[i]=(fabs(dxu[i])+fabs(dyu[i])+fabs(dzu[i]))/3
        logdr[i]=log10(dru[i])
    else:
        dru[i]=0.5*(fabs(dxu[i])+fabs(dyu[i]))
        logdr[i]=log10(dru[i])



n,bins,patches=plt.hist(logdr,bins=100,range=(0,4))

f=open("van-hove-hist-%d.txt"%dts,"w")
for j in range(100):
    f.write("%d %f\n"%(n[j],bins[j]))

f.close()

plt.xlabel("log10")
plt.ylabel("displacement")
plt.title("van_hove_function")
plt.savefig("van-hove-%d.png"%dts)

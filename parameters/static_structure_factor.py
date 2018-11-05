#! /usr/bin/env python

import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
import scipy.special
#import matplotlib.pyplot as plt


###################################################################################
gdot   = 0.001
dim    = 3
verbose= False
# ##################################################################################

###################################################################################
if(size(sys.argv)<2) :
    sys.stderr.write('Usage : i.     dump_file\n')
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

tsrt = sys.argv[carg]
carg += 1

###################################################################################

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
    num_particle =lstr.nb_atoms
else:
    print tsrt, " does not exist. "



k=zeros(200)
for i in range(200):
    #k[i]=4*pi/L+i*(30-4*pi/L)/200
    k[i]=2*pi/L+i*2*pi/L
sk=zeros(200)
sksum=zeros(200)
kk=zeros(200)
bessel=zeros(200)


for i in range(num_particle-1):
    for j in range(i,num_particle):
        if dim==3:
            rij= sqrt((lstr.x[i]-lstr.x[j])**2+(lstr.y[i]-lstr.y[j])**2+(lstr.z[i]-lstr.z[j])**2)
        else:
            rij= sqrt((lstr.x[i]-lstr.x[j])**2+(lstr.y[i]-lstr.y[j])**2)

        #for q in range(200):
        #    kk[q]=k[q]*rij
        kk=k*rij
        bessel=scipy.special.jv(0,kk)
        sksum+=bessel
        #for q in range(200):
        #    sksum[q]+=bessel[q]

sk=1+sksum/num_particle
f=open('ssf_%d.txt'%ts0,'w')
x=argmax(sk)
print k[x],sk[x]

for q in range(200):
    f.write("%f %f\n"%(k[q],sk[q]))
f.close()

#plt.plot(k,sk)
#plt.xlabel("k")
#plt.ylabel("s(k)")
#plt.title("static_structure_factor")
#plt.show()

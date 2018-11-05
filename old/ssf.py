#! /usr/bin/env python

import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
import scipy.special
#import matplotlib.pyplot as plt

pathdir = os.environ['HOME']+'/mols/misc_scripts'
sys.path.append(pathdir)


###################################################################################
gdot   = 0.001
dim    = 3
verbose= False
# ##################################################################################

###################################################################################
if(size(sys.argv)<2) :
    sys.stderr.write('Usage : i.     start_dump_file\n')
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


tsrt = int(sys.argv[carg])
carg += 1
###################################################################################
def function(tsrt):
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


    qmin = 2*pi/L
    qmax = 4*pi
    sample= int(qmax/qmin)
    #print sample
    kx=arange(1,sample+1)
    ky=arange(1,sample+1)
    kz=arange(1,sample+1)
    q_m=zeros((sample,sample,sample))
    sq=zeros((sample,sample,sample))
    k_list=[]
    #print kx

    for i in range(len(kx)):
        for j in range(len(ky)):
            for k in range(len(kz)):
                q_m[i][j][k]=sqrt(((2*pi/L)**2)*(kx[i]**2+ky[j]**2+kz[k]**2))
                k_list.append(kx[i]**2+ky[j]**2+kz[k]**2)
                cossum=0.0
                sinsum=0.0
                for l in range(num_particle):
                    cossum+=cos(lstr.x[l]*kx[i]*(2*pi/L)+lstr.y[l]*ky[j]*(2*pi/L)+lstr.z[l]*kz[k]*(2*pi/L))
                    sinsum+=sin(lstr.x[l]*kx[i]*(2*pi/L)+lstr.y[l]*ky[j]*(2*pi/L)+lstr.z[l]*kz[k]*(2*pi/L))
                sq[i][j][k]=(cossum**2+sinsum**2)/num_particle

    k_list.sort()
    k_clear_list=list(set(k_list))
    #print k_clear_list
    k2=asarray(k_clear_list)

    sq_avg=zeros(len(k2))

    for m in range(len(k2)):
        count=0
        sq_sum=0
        for i in range(len(kx)):
            for j in range(len(ky)):
                for k in range((len(kz))):
                    if kx[i]**2+ky[j]**2+kz[k]**2 == k2[m]:
                        sq_sum+=sq[i][j][k]
                        count+=1
                        sq_avg[m]=sq_sum/count
    q=zeros(len(k2))
    for i in range(len(k2)):
        q[i]=(2*pi/L)*sqrt(k2[i])
    return q,sq_avg

###################################################################################
step=tsrt
dsrt= 'dumpfile.'+str(step).zfill(10)+'.txt'
x,y=function(dsrt)

for kk in range(len(x)):
    print x[kk], y[kk]
###################################################################3

'''

## below is a simplfied version that assume kx ky kz is always the same and grow together
#print L


qmin = 2*pi/L
qmax = 4*pi
m = int(qmax/qmin)
k=arange(1,m+1)
qq=zeros(m*m*m)
sq=zeros(m*m*m)
a=0

for i in range(m):
    for j in range(m):
        for k in range(m):
            cossum=0.0
            sinsum=0.0
            qx = i*qmin
            qy = j*qmin
            qz = k*qmin
            for l in range(num_particle):
                cossum += cos( qx*lstr.x[l]+qy*lstr.y[l]+qz*lstr.z[l])
                sinsum += sin( qx*lstr.x[l]+qy*lstr.y[l]+qz*lstr.z[l])

            sq[a]=(cossum**2+sinsum**2)/num_particle
            qq[a] = sqrt(qx*qx+qy*qy+qz*qz)
            a=a+1


#f=open('ssf2_%d.txt'%ts0,'w')

'''
#for i in range(len(k2)):
    ##print qq[i],sq[i]
    #print (2*pi/L)*sqrt(k2[i]),sq_avg[i]
    #f.write("%f %f\n"%(q_m[i],sq[i]))

#f.close()

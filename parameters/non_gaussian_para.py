#! /usr/bin/env python
#non_gaussian parameter is a quantity of every datas to see whether the distribution is a gaussian or not

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
            dru[i]=sqrt(dxu[i]**2+dyu[i]**2+dzu[i]**2)
        else:
            dru[i]=sqrt(dxu[i]**2+dyu[i]**2)

    return dxu,dyu,dzu,dru,num_particle
###################################################################################
if(size(sys.argv)<2) :
    sys.stderr.write('Usage : i.    starting time\n')
    sys.stderr.write('        ii.   interval\n')
    sys.stderr.write('        iii.   ending time\n')
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
ivals  = int(sys.argv[carg])
carg += 1
tend  = int(sys.argv[carg])
carg += 1
###################################################################################

total_file=(tend-tsrt)/ivals
print total_file
step=tsrt
for i in range(1,total_file+1):
    dsrt= 'dumpfile.'+str(step).zfill(10)+'.txt'
    step=tsrt+i*ivals
    dend='dumpfile.'+str(step).zfill(10)+'.txt'
    newx,newy,newz,newr,num_particle=onefile(dsrt,dend)
    if i==1:
        dxu=newx
        dyu=newy
        dzu=newz
        dru=newr
    else:
        dxu=concatenate((dxu,newx),axis=0)
        dyu=concatenate((dyu,newy),axis=0)
        dzu=concatenate((dyu,newz),axis=0)
        dru=concatenate((dzu,newr),axis=0)




#n,bins,patches=plt.hist(dxu,bins=100,range=(-100,100))
#plt.savefig("hist_dx.png")
#print(dxu)
ave_dr =  mean(dru)
ave_dxu= mean(dxu)
ave_dyu= mean(dyu)
if dim==3:
    ave_dzu= mean(dzu)

print "ave of dx ",ave_dxu
print "ave of dy", ave_dyu
print "ave of dr", ave_dr

if dim==3:
    print "ave of dz", ave_dzu


sample=num_particle*total_file
dx2=zeros(sample)
dx4=zeros(sample)
dy2=zeros(sample)
dy4=zeros(sample)
dz2=zeros(sample)
dz4=zeros(sample)
dr2=zeros(sample)
dr4=zeros(sample)

#print "sample",sample
#print shape(dxu)

for i in range(sample):
    dxu[i]-=ave_dxu
    dx2[i]=dxu[i]**2
    dx4[i]=dxu[i]**4
    dyu[i]-=ave_dyu
    dy2[i]=dyu[i]**2
    dy4[i]=dyu[i]**4
    dru[i]-=ave_dr
    dr2[i]=dru[i]**2
    dr4[i]=dru[i]**4
    if dim==3:
        dzu[i]-=ave_dzu
        dz2[i]=dzu[i]**2
        dz4[i]=dzu[i]**4

if dim == 3:
    NGP_dx=(2*mean(dx4))/(3*mean(dx2)**2)-1
    NGP_dy=(2*mean(dy4))/(3*mean(dy2)**2)-1
    NGP_dz=(2*mean(dz4))/(3*mean(dz2)**2)-1
    NGP_r=(2*mean(dr4))/(3*mean(dr2)**2)-1

    print  "NGP_r",NGP_r
    print  "NGP_dx",NGP_dx
    print  "NGP_dy",NGP_dy
    print  "NGP_dz",NGP_dz
else:
    NGP_dx=(2*mean(dx4))/(3*mean(dx2)**2)-1
    NGP_dy=(2*mean(dy4))/(3*mean(dy2)**2)-1
    NGP_r=(2*mean(dr4))/(3*mean(dr2)**2)-1
    print  "NGP_r",NGP_r
    print  "NGP_dx",NGP_dx
    print  "NGP_dy",NGP_dy

f=open("data-displacement-ival%d.txt"%ivals,'w')
for i in range(sample):
    f.write('%f %f %f %f\n'%(dxu[i],dyu[i],dzu[i],dru[i]))
f.close()


n,bins=histogram(dxu,bins=50,density=True)
fx=open("hist-dx-ival%d.txt"%ivals,"w")
for j in range(50):
    fx.write("%f %f\n"%(bins[j],n[j]))
fx.close()

######################################################################
# would like to make the data more symmtriy
# dxu-minus is the negative array of the original dxu
dxu_minus= -dxu
dyu_minus= -dyu
dzu_minus= -dzu

#this array record all the displacement on all the direction
displacement_xyz= concatenate((dxu,dyu,dzu,dxu_minus,dyu_minus,dzu_minus),axis=0)

n1,bins1=histogram(displacement_xyz,bins=50,density=True)
fxyz=open("plot-6xyz-ival%d.txt"%ivals,"w")
for j in range(50):
    fxyz.write("%f %f\n"%(bins1[j]+(bins1[2]-bins1[1])/2.0,n1[j]))

fxyz.close()

'''
n,bins,patches=plt.hist(dyu,bins=100)
plt.title('NGP_dy %f'%NGP_dy)
fy=open("hist-dy-ival%d.txt"%ivals,"w")
for j in range(100):
    n[j]/=sum(n)
    fy.write("%f %f\n"%(n[j],bins[j]))
fy.close()
plt.savefig("hist-dy-ival%d.png"%ivals)
n,bins,patches=plt.hist(dzu,bins=100)
plt.title('NGP_dz %f'%NGP_dz)
fz=open("hist-dz-ival%d.txt"%ivals,"w")
for j in range(100):
    n[j]/=sum(n)
    fz.write("%f %f\n"%(n[j],bins[j]))
fz.close()
plt.savefig("hist-dz-ival%d.png"%ivals)
'''

n,bins,patches=plt.hist(dru,bins=100)
plt.title('NGP_dr %f'%NGP_r)
fr=open("hist-dr-ival%d.txt"%ivals,"w")
for j in range(100):
    fr.write("%f %f\n"%(bins[j],n[j]))
fr.close()
plt.savefig("hist-dr-ival%d.png"%ivals)

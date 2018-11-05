# this is version one, measure on real space
import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
from math import *
###########################################################################
# pre define parameters
dim  = 3
verbose= False
bool_func= 0
dt =0.00004
##########################################################################
if(size(sys.argv)< 1):
    sys.stderr.write('Usage : i. start dumpfile\n')
    sys.stderr.write('Usage : ii. second dumpfile\n')
    sys.stderr.write('Usage : iii. bin number\n')
    print
    exit()

carg =1

for word in sys.argv[carg:]:
        if word == "-dt":
            carg += 1
            dt = float(sys.argv[carg])
            carg += 1
        if word == "-dim":
            carg += 1
            dim = int(sys.argv[carg])
            carg += 1
        if word == "func":
            carg += 1
            bool_func = int(sys.argv[carg])
            carg += 1

dsrt = sys.argv[carg]
carg += 1
dend = sys.argv[carg]
carg += 1
bin = int(sys.argv[carg])
carg += 1
##########################################################################
# read one file to extract the information of d_directorx d_directory d_directorz
if os.path.exists(dsrt):
    if dim==3:
        lstr  = LammpsOperations()
        lstr.readFile3d(dsrt, verbose)
    else:
        lstr  = LammpsOperations()
        lstr.readFile(dsrt, verbose)
    num_particle =lstr.nb_atoms
else:
    print dsrt, " does not exist."

if os.path.exists(dend):
    if dim==3:
        lend  = LammpsOperations()
        lend.readFile3d(dend, verbose)
    else:
        lend  = LammpsOperations()
        lend.readFile(dend, verbose)
else:
    print dend, " does not exist."
#############################################################################
dx=zeros(num_particle)
dy=zeros(num_particle)
dz=zeros(num_particle)
radius=zeros(num_particle)
dtime = (lend.tsteps- lstr.tsteps)
L = lstr.cell[1]
for i in range(num_particle):
     dx[i] = lend.xu[i] - lstr.xu[i]
     dy[i] = lend.yu[i] - lstr.yu[i]
     dz[i] = lend.zu[i] - lstr.zu[i]
     radius[i] = lstr.rad[i]
###########################################################################
# displacement correlations
def velocity_cor(lstr,lend,bin,L,dx,dy,dz):
    ### create a class to store it
    binbound = linspace(1, sqrt(3)*L/2,bin)
    binsize = binbound[1]-binbound[0]
    print(binbound)
    print(binsize)
    corr_displacement=zeros(bin)
    n_r=zeros(bin)
    c=0
    for i in range(num_particle):
        c=c+dx[i]*dx[i]+dy[i]*dy[i]+dz[i]*dz[i]
    c= c/num_particle

    for i in range(num_particle):
        for j in range(i+1,num_particle): # didn't consider the situation of j = i
            rx=lstr.x[i]-lstr.x[j]
            if abs(rx) > L/2 :  #solve the cross boundary problem
                rx= L - abs(rx)    # rx is always smaller than half of the system size
            ry=lstr.y[i]-lstr.y[j]  # so this correlation is from one diameter size to sqrt(3)*L/2
            if abs(ry) > L/2 :
                ry= L - abs(ry)
            rz=lstr.z[i]-lstr.z[j]
            if abs(rz) > L/2 :
                rz= L - abs(rz)
            rij=sqrt(rx**2+ry**2+rz**2)
            #print drij
            #print "dx=",dx,"dy=",dy,"dz=",dz
            d2ij=dx[i]*dx[j]+dy[i]*dy[j]+dz[i]*dz[j]  # if direction of self-propeling and velocity
            corr_displacement[int((rij-1)/binsize)]+=d2ij # this first bin is start from 1 instead of 0
            n_r[int((rij-1)/binsize)]+=1  # sum up number of particle in this range
    f1= open('bin_corr_%d_%d.txt'%(dtime,bin),'w')
    for i in range(bin):
        if n_r[i]==0:
            corr_displacement[i]=0
        else:
            corr_displacement[i]=corr_displacement[i]/(n_r[i]*c)
        f1.write('%1.6f %1.6f\n'%(binbound[i]+binsize/2,corr_displacement[i]))

    return corr_displacement,binbound,binsize
##############################################################################
#print out the information in a file
corr_displacement,binbound,binsize=velocity_cor(lstr,lend,bin,L,dx,dy,dz)
##########################################################################
#this is a global parameter
def global_p(corr_displacement,binbound,binsize):
    sum=0
    for i in range(len(corr_displacement)):
        r = binbound[i]+binsize/2
        if r > L/2:
            break
        sum= sum+4*pi*r*r*corr_displacement[i]
    kai = num_particle*sum/(L*L*L)
    return kai

if bool_func == 1:
    f2 = open('global_correlation.txt','a')
    f2.write('%f \n'%global_p(corr_displacement,binbound,binsize))
    f2.close()
#vicsek

##############################################################################
# plot it out
def plot():
    plt.plot(binb,correlations)
    plt.show()

#plot()
##############################################################################
# print the information in a separate file

def printdata(lstr,lend,dx,dy,dz,radius):
    f= open('displacement-%d.txt'%dtime,'w')
    #f.write()
    for i in range(num_particle):
        f.write("%d %1.6f %1.6f %1.6f %1.6f %1.6f %1.6f %1.6f\n"%(i+1,lstr.x[i],lstr.y[i],lstr.z[i],dx[i],dy[i],dz[i],radius[i]))
    f.close()


printdata(lstr,lend,dx,dy,dz,radius)

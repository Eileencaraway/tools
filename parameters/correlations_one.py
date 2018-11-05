# this is version one, measure on real space
import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp2 import *
from scipy import *

###########################################################################
dim  = 3
verbose= False
###########################################################################

if(size(sys.argv)< 1):
    sys.stderr.write('Usage : i. dumpfile\n')
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
##########################################################################
# read one file to extract the information of d_directorx d_directory d_directorz
if os.path.exists(dsrt):
    if dim==3:
        lstr  = LammpsOperations()
        lstr.readFile3d(dsrt, verbose)
    else:
        lstr  = LammpsOperations()
        lstr.readFile(dsrt, verbose)

    ts     = lstr.tsteps
    L       = lstr.cell[1]
    num_particle =lstr.nb_atoms
else:
    print tsrt, " does not exist."
#############################################################################
# first type of velocity corelation
# velocity correlation
def velocity_cor():
    bin = 100
    #print L/2
    #print sqrt(3)*L/2
    binsize = (sqrt(3)*L/2)/bin
    #print binsize
    binbound = arange(0,sqrt(3)*L/2+binsize,binsize)
    corr_velocity=zeros(bin)
    corr_director=zeros(bin)
    n_r=zeros(bin)

    for i in range(num_particle):
        for j in range(i+1,num_particle):
            dx=lstr.x[i]-lstr.x[j]
            if abs(dx) > L/2 :  #solve the cross boundary problem
                dx= L - abs(dx)
            dy=lstr.y[i]-lstr.y[j]
            if abs(dy) > L/2 :
                dy= L - abs(dy)
            dz=lstr.z[i]-lstr.z[j]
            if abs(dz) > L/2 :
                dz= L - abs(dz)
            drij=sqrt(dx**2+dy**2+dz**2)  #displacement
            #print drij
            #print "dx=",dx,"dy=",dy,"dz=",dz
            dir2ij=lstr.dirx[i]*lstr.dirx[j]+lstr.diry[i]*lstr.diry[j]+lstr.dirz[i]*lstr.dirz[j]  # if direction of self-propeling and velocity
            v2ij=lstr.vx[i]*lstr.vx[j]+lstr.vy[i]*lstr.vy[j]+lstr.vz[i]*lstr.vz[j]
            corr_velocity[int(drij/binsize)]+=v2ij  # sum up the v2ij in this bin range
            corr_director[int(drij/binsize)]+=dir2ij # direction
            n_r[int(drij/binsize)]+=1  # sum up number of particle in this range

    for i in range(bin):
        #print "corr_r=",corr_r[i],"n_r=",n_r[i]
        if n_r[i]==0:
            corr_v[i]=0
        else:
            corr_v[i]=corr_v[i]/n_r[i]
            corr_d[i]=corr_d[i]/n_r[i]
        print binbound[i+1], corr_v[i],corr_d[i]


##########################################################################
# direction correlation

#############################################################################
#vicsek order parameter
#this is a global parameter
def vicsek():
    v0=zeros(num_particle)
    sum_vx=0
    sum_vy=0
    sum_vz=0
    sum_v0=0
    for i in range(num_particle):
        v0[i]=sqrt(lstr.vx[i]*lstr.vx[i]+lstr.vy[i]*lstr.vy[i]+lstr.vz[i]*lstr.vz[i])
        sum_vx+=lstr.vx[i]
        sum_vy+=lstr.vy[i]
        sum_vz+=lstr.vz[i]
        sum_v0+=v0[i]

    phi= sqrt(sum_vx*sum_vx + sum_vy*sum_vy + sum_vz*sum_vz)/sum_v0

    return phi

if bool_func == 1:
    print vicsek()
#vicsek
##############################################################################

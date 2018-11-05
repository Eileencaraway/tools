from scipy import *
import re
from math import *
import matplotlib.pyplot as plt
import sys
import os
from lammpsOperationsnp import *


pathdir = os.environ['HOME']+'/Dropbox/Code/tools/'
sys.path.append(pathdir)

###################################################################################
dt     = 0.000444288
gdot   = 0.001
dim    = 3
verbose= False
# ##################################################################################
if(size(sys.argv)<2) :
    sys.stderr.write('Usage : i.    dumpfile \n')
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

dumpfile = int(sys.argv[carg])
carg += 1

dsrt='dumpfile.'+str(int(dumpfile)).zfill(10)+'.txt'
#####################################################################
if os.path.exists(dsrt):
    if dim==3:
        lstr  = LammpsOperations()
        lstr.readFile3d(dsrt, verbose)
    else:
        lstr  = LammpsOperations()
        lstr.readFile(dsrt, verbose)

    ts0     = lstr.tsteps
    L       = lstr.cell[1]
    num_particle = lstr.nb_atoms
else:
    print tsrt, " does not exist."

#initialize
particles=zeros((num_particle,3))
rho=num_particle/(L*L*L)
nbins=1000
g=zeros(nbins)
########################################################
# this part is for read particles position
def read(dsrt):
    # this is a matrix contain x y z postions of all the particles
    positions=zeros((num_particle,3))

    for i in range(num_particle):
        positions[i][0]=lstr.x[i]
        positions[i][1]=lstr.y[i]
        if dim==3:
            positions[i][2]=lstr.z[i]

    return positions
##########################################
##switch=0 initialize switch=1 sample switch=2 result
def gr(switch):
    global ngr,bin_size,nbins,g
    if(switch==0):
        ngr=0
        print("ngr is initialized")
        bin_size=L/(2*nbins)
        for i in range(nbins):
            g[i]=0

    elif(switch==1):
        ngr+=1  ## ngr number of times to calculate gr
        for i in range(num_particle-1):
            for j in range(i+1,num_particle):
                dx=particles[i][0]-particles[j][0]
                dy=particles[i][1]-particles[j][1]
                dz=particles[i][2]-particles[j][2]
                #print(dx)
                dx -=  L*round(dx/L)
                dy -=  L*round(dy/L) ## L is the size of the box at x and at y
                dz -=  L*round(dz/L)
                r2 = dx*dx + dy*dy + dz*dz
                if(r2<L*L/4):
                    #print(r2)
                    r = sqrt(r2)
                    ig = int(r/bin_size)
                    g[ig]+=1
                #print(gr)

    elif((switch==2)&(ngr!=0)):
        outfile=open('RDF.dat','w')
        radius=zeros(nbins)
        for i in range(nbins):
            radius[i] = (i+0.5)*bin_size;
            ## area=*pi*bin_size*bin_size*((i+1)*(i+1)-i*i)*rho
            vol = (4/3)*pi*bin_size*bin_size*bin_size*((i+1)*(i+1)*(i+1)-i*i*i)*rho
            #print(g[i])
            #g[i]=g[i]/area
            g[i] = 2*g[i]/(ngr*vol*num_particle)
            #print(g[i])
            outfile.write(str(radius[i])+" "+str(g[i])+"\n")

        plt.plot(radius,g)
        plt.savefig("radial_distribution.png")
        outfile.close()

gr(0)
particles=read(dsrt)
gr(1)
gr(2)

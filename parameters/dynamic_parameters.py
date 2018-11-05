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
dt     = 0.001
gdot   = 0.001
verbose= False
# ##################################################################################

###################################################################################
if(size(sys.argv)<4) :
    sys.stderr.write('Usage : i.    starting dump_file\n')
    sys.stderr.write('        ii.   ending dump_file\n')
    sys.stderr.write('        iii.  timestep intervals\n')
    sys.stderr.write('        iv.   parameters\n')
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

tsrt = sys.argv[carg]
carg += 1
tend  = sys.argv[carg]
carg += 1
ivals = float(sys.argv[carg])
carg += 1
function = sys.argv[carg]
carg += 1
###################################################################################

lstr  = LammpsOperations()
lstr.readFile(tsrt, verbose)
lend  = LammpsOperations()
lend.readFile(tend, verbose)

###################################################################################




def van_hove_func(lstr, lend):
    for i in num_particle:
        dxu[i]=lstr.xu[i]-lend.xu[i]
        dyu[i]=lstr.yu[i]-lend.yu[i]
        duxduy[i]=0.5*(fabs(dxu[i])+fabs(dyu[i]))

    logdxdy=np.log10(duxduy)

    plt.hist(logdxdy,1,10)
    plt.xlabel("log10")
    plt.ylabel("displacement")
    plt.title("van_hove_function")
    plt.show()

def gr(switch):

    lop  = LammpsOperations()
    lop.readFile(dumpfile, verbose)

    L=lop.cell[1]
    num_particle=lop.nb_atoms
    rho=num_particle/(L*L)
    nbins=500
    g=zeros(nbins)

    global ngr,bin_size,nbins,g
    if(switch==0):
        ngr=0
        print("ngr is initialized")
        bin_size=L/(2*nbins)
        for i in range(nbins):
            g[i]=0

    elif(switch==1):
        ngr+=1  ## ngr number of times to calculate gr
        for i in range(num_bacteria-1):
            for j in range(i+1,num_particle):
                dx=lop.ux[i]-lop.ux[j]
                dy=lop.uy[i]-lop.uy[j]
                #print(dx)
                dx -=  L*round(dx/L)
                dy -=  L*round(dy/L) ## L is the size of the box at x and at y
                r2 = dx*dx + dy*dy
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
            area = pi*bin_size*bin_size*((i+1)*(i+1)-(i)*(i))*rho
            #print(g[i])
            #g[i]=g[i]/area
            g[i] = 2*g[i]/(ngr*area*num_particle)
            #print(g[i])
            outfile.write(str(radius[i])+" "+str(g[i])+"\n")

        plt.plot(radius,g)
        plt.show()
        outfile.close()

def sk(dumpfile):
    L=lop.cell[1]
    k=arange(4*pi/L,30,200)
    sk=zeros(200)
    for q in range(200):
        for i in range(num_particle):
            for j in range(num_particle):
                rij= sqrt((lop.x[i]-lop.x[j])**2+(lop.y[i]-lop.y[j])**2)
                if j!=i:
                    sksum[q]+=scipy.special.jv(0,k[q]*rij)
        sk[q]=1+sksum[q]/num_particle

def incoherent_intermediate_scattering_func(dumpfile_s, dumpfile_e,q):
    lstr    = LammpsOperations()
    lend    = LammpsOperations()
    lstr.readFile(dumpfile_s, verbose)
    lend.readFile(dumpfile_e, verbose)
    num_particle=lstr.nb_atoms
    for i in range(num_particle):
        dx=lend.ux[i]-lstr.ux[i]
        dy=lend.uy[i]-lstr.uy[i]
        isf+=cos(kx*dx+ky*dy)

    return isf/num_particle


def four_point_suseptibility():


def non_gaussian_parameters():

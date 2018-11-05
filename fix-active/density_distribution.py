from scipy import *
import numpy as np
import matplotlib.pyplot as plt
import sys
from lammpsOperationsnp import *
import math

if(size(sys.argv)<3):
    sys.stderr.write('please type in: 1. the resolution (int = L/small box length) \n')
    sys.stderr.write('                2. nbins (need to be a int value)  \n')
    exit()
n = int(sys.argv[1])
nbins = int(sys.argv[2])
verbose = False
dim = 3
# read dumpfiles , so use joyjit's class
def readfile(filename):
    # select snap ids corresponding to timesteps
    if os.path.exists(filename):
        if dim==3:
            lstr  = LammpsOperations()
            lstr.readFile3d(filename, verbose)
        else:
            lstr  = LammpsOperations()
            lstr.readFile(filename, verbose)

        ts0     = lstr.tsteps
        L       = lstr.cell[1]
        num_particle =lstr.nb_atoms
    else:
        print filename, " does not exist. "
    # paramater l is the box length,  l = L/2, L/3, L/4, ..., L/n
    # then number of small box is n^3
    l = L/n # l is the small box length
    #n = L/l
    #print("l = %f"%l)
    m = n**3 # m is the number of small box in the system
    count = zeros((n,n,n)) # initialize the counts for each boxs
    # read the
    for i in range(num_particle):
        #print(i+1,lstr.x[i],lstr.y[i],lstr.z[i],L)
        # solve the boundary problem
        if lstr.x[i]>L:
            lstr.x[i]-=L
        if lstr.x[i]<0:
            lstr.x[i]+=L
        if lstr.y[i]>L:
            lstr.y[i]-=L
        if lstr.y[i]<0:
            lstr.y[i]+=L
        if lstr.z[i]>L:
            lstr.z[i]-=L
        if lstr.z[i]<0:
            lstr.z[i]+=L
        # exam which box the particle below to
        ix=int(lstr.x[i]/l)  # because we don't have minus value, we can use int
        iy=int(lstr.y[i]/l)  # otherwise, use math.floor()
        iz=int(lstr.z[i]/l)
        count[ix][iy][iz]= count[ix][iy][iz]+1


    count_array = np.reshape(count,m,order='F')
    #print(count)
    density = count_array*(4*math.pi*(0.5**3)/3)/(l**3)

    return density

# create a list of filenames, which now I choose as the files to do average
# they are separated enough, they are all in steady state
list = []
for i in range(1,10):
    timestep = i*1000000
    list.append('dumpfile.'+str(timestep).zfill(10)+'.txt')
for i in range(1,11):
    timestep = i*10000000
    list.append('dumpfile.'+str(timestep).zfill(10)+'.txt')
#print(list)
############################################################################
#calculate distribution
hist = zeros((len(list),nbins))
for i in range(len(list)):
    boxs_density = readfile(list[i])
    #print(boxs_density)
    hist[i], bin_edges = np.histogram(boxs_density,bins= nbins, range =(0.0, 0.7), density=True)
    bin_size = bin_edges[1]-bin_edges[0]

val = np.mean(hist,axis=0) # after average over different files
#print(val)
#############################################################################3
#output a plot, and a file saving the distribution
f=open('density_distribution_n%d.dat'%n,'w')

for i in range(len(val)):
    f.write('%1.4f %1.4f \n'%(bin_edges[i]+bin_size/2,val[i]))

plt.plot(bin_edges[:nbins]+bin_size/2,val)
plt.xlabel('density')
plt.ylabel('probability')
plt.show()
plt.savefig('density_distribution_n%d.png'%n)

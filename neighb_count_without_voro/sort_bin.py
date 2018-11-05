## this code is used for read a list of number and output the distribution
## input file , number of bin,
## output max, min, the distribution
import scipy
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import StringIO
import re
import scipy.stats
##################################################
#read the file from the command line
if(len(sys.argv)<2):
    sys.stderr.write('Usage : i. filename\n')
    sys.stderr.write('        ii. number of bins\n')
    sys.stderr.write('        iii. Title\n')
    exit()
##sys.argv first argv is the python file, if you want to
##input the filename, filename is the 2rd argv
carg = 1
file  = str(sys.argv[carg])
carg += 1
nbins = int(sys.argv[carg])
carg +=1
tit  = str(sys.argv[carg])
########################################################

def readfile(file):

    f = open(file,'r')
    # read the first colunms and the second columns
    col1 =[]
    col2 =[]
    for line in f:
        num = line.split()
        col1.append(int(num[0]))  # id of the particles
        col2.append(float(num[1]))  # local density of particles
    col_matrix = np.array([col1,col2])
    #print(col_matrix)
    return col_matrix
#######################################################
col_matrix = readfile(file)
#val,bin_edges = np.histogram(col_matrix[1],nbins)
val,bin_edges,patches = plt.hist(col_matrix[1],nbins)
bin_size = bin_edges[1]-bin_edges[0]
#plt.show()
plt.xlabel('local density')
plt.ylabel('number of particles')
plt.title(tit)
plt.savefig("distribution.png")
#######################################################
def savefile(val,bin_edges):
    save = 'bin-'+file
    print (save)
    f2 = open(save,'w')
    for i in range(len(val)):
        f2.write('%f %f \n'%(bin_edges[i],val[i]))
    f2.write('%f\n'%bin_edges[-1])

savefile(val,bin_edges)
#######################################################
#save two parameters: Sarle's bimodality coefficient b, average fraction P of particle in cluster
def stat(val,bin_edges):
    skew = scipy.stats.skew(col_matrix[1])
    kurtosis = scipy.stats.kurtosis(col_matrix[1])
    sarle = (skew**2+1)/(kurtosis+3*(nbins-1)**2/((nbins-2)*(nbins-3)))
    print("skew=%1.2f"%skew)
    print("kurtosis=%1.2f"%kurtosis)
    print("sarle=%1.2f"%sarle)
    # cluster fraction of the largest cluster if it phase separated
    # two peak
    ntotal = len(col_matrix[1])
    ncluster = 0
    P = 0
    if (sarle >= 0.55):
        for i in range(len(val)):
            if bin_edges[i]+bin_size/2> 0.4:
                ncluster += val[i]
        P = ncluster/ntotal
    print("cluster fraction P = %1.2f"%P)
stat(val,bin_edges)

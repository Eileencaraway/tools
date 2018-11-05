from scipy import *
import scipy
import numpy as np
import os
import sys
import StringIO
import re


##################################################
#read the file from the command line
if(len(sys.argv)<2):
    sys.stderr.write('Usage : i. filename\n')
    sys.stderr.write('        ii. gas cut\n')
    sys.stderr.write('        iii. cluster cut\n')
    exit()
##sys.argv first argv is the python file, if you want to
##input the filename, filename is the 2rd argv
carg = 1
file = str(sys.argv[carg])
carg += 1
gcut = int(sys.argv[carg])
carg +=1
ccut = int(sys.argv[carg])
########################################################

particle = zeros((10000,3))
f = open(file,'r')
# read the first colunms and the second columns
gas_ID = []
cluster_ID = []
gas_local_density = []
cluster_local_density = []
for line in f:
    num = line.split()
    if(int(num[2])<=3):
        print("this is a gas particle, save it")
        print("the particle id is %d"%int(num[0]))
        gas_ID.append(int(num[0]))
        gas_local_density.append(float(num[1]))  #
    elif(int(num[2])>=11):
        cluster_ID.append(int(num[0]))
        cluster_local_density.append(float(num[1]))

##############################################
#save into file
f2 = open('gas_id.dat','w')
for i in range(len(gas_ID)):
    f2.write('%d %1.6f \n'%(gas_ID[i]+1,gas_local_density[i]))

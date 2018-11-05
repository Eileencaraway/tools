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
dt     = 0.000444288
gdot   = 0.001
k      = 7.361444
dim    = 3
verbose= False
tau    = 913  ## for phi0.1 mu0.5
# ##################################################################################
###################################################################################
if(size(sys.argv)<1) :
    sys.stderr.write('        i.   filename \n')
    print
    exit()

carg = 1
filename = str(sys.argv[carg])
carg += 1

ISF=zeros((2,63))

f=open(filename)
count=0
for line in f:
    if count<63:
        num=line.split()
        ISF[0,count]=num[0]
        ISF[1,count]=num[1]
        count+=1

value=zeros(63)
for i in range(63):
    value[i]=abs(ISF[1,i]-0.367879)


print("tau=%f"%ISF[0,argmin(value)])

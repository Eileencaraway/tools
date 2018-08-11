#!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

L = sys.argv
first = 0
values = 0
sq_values = 0
sum_column = 0

def notStr(List):
    num=True
    try:
        float(List[0])
    except ValueError:
        num=False
    if num:
        return True
    else:
        try:
            float(List[1])
        except ValueError:
            num=False
    
    return num

for filename in sys.argv[1:]:
    if not os.path.exists(filename):
        continue

    f = open(filename)
    data = f.readlines()
    List = []
    for j in range(0, len(data)):
        if not (data[j].startswith("#") or data[j].startswith("\n")) :
        #if notStr(data[j]) :
            tmp = fromstring(data[j],sep="   ")
            List.append(tmp)
            
    if first == 0:
        Sum_List = List
        l = array(List)
        Sqsum_List = l*l
        length = len(Sum_List)
        No_files = 1
        first = 1
    else:
        if len(List)==length:
            No_files +=1
            l = array(List)
            Sum_List += l 
            Sqsum_List += l*l
            
            
    sys.stderr.write('import '+filename+' size-'+str(len(List))+'\n')
    f.close()

sys.stderr.write('No_files = '+str(No_files)+'\n')
Sumsq = array(Sum_List)
Sumsq_List = (Sumsq*Sumsq)
#print Sumsq_List
#print Sqsum_List
computeError = (No_files*Sqsum_List - Sumsq_List)/No_files/No_files
#print computeError

for i in range(0, length):
    for j in range(0, len(Sum_List[i])):
        if computeError[i][j]<0:
            computeError[i][j] = -1.0*computeError[i][j]
        print Sum_List[i][j]/No_files, math.sqrt(computeError[i][j]),
    print
    sum_column += Sum_List[i]
    values = Sum_List[i]
    sq_values += values*values
    #print sum_column, sq_values
    
    
result = zeros([1, 2*len(tmp)], 'f') 
for i in range(0, len(tmp)):
    average = sum_column[i]/(No_files*length)
    variance = sq_values[i]/(No_files*No_files*length) - average*average
    if variance<0:
        variance = -1.0*variance
    stddev = math.sqrt(variance)
    result[0][2*i] = average
    result[0][2*i+1] = stddev
    
print "#Meanvalues and #variance = ", 
for j in range(0, len(result[0])):
    print result[0][j],
    
    


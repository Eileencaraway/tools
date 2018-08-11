 #!/usr/bin/env python

import sys
import os
import math
import numpy
from numpy import *

first        = 0
No_files     = 0
No_rows      = 0
sum_fileData = []

def notStr(List):
    num=True
    try:
        float(List[0])
    except ValueError:
        num=False

    if num:
        return True

    try:
        float(List[1])
    except ValueError:
        return False

for filename in sys.argv[1:]:
    if not os.path.exists(filename):
        continue

    f = open(filename)
    data = f.readlines() ## read all the lines in a file
    f.close()
    List = []

    for j in range(0, len(data)):
        if not (data[j].startswith("#") or data[j].startswith("\n") or data[j].startswith('ERROR')) :
        #if notStr(data[j]) :
            tmp = fromstring(data[j],sep=" ") # separate a string by " " space, tmp is an array
            List.append(tmp)

    if len(List) < 1:
        continue

    if first == 0:
        l = array(List)  # change List to array
        Sum_List = l
        #Sqsum_List = l*l
        No_rows = len(Sum_List)  # number of rows
        No_columns = len(Sum_List[0])
        No_files = 1
        Sum_Line = 0
        for i in range(0,  No_rows):
            Sum_Line += l[i]
        sum_fileData.append(Sum_Line)
        first = 1
    else:
        if len(List)== No_rows:
            No_files +=1
            l = array(List)  # matrix
            Sum_List += l  # this is a matrix + matrix
            #Sqsum_List += l*l
            Sum_Line = 0
            for i in range(0,  No_rows):
                Sum_Line += l[i]

            sum_fileData.append(Sum_Line)


    sys.stderr.write('#import '+filename+' size-'+str(len(List))+'\n')

sys.stderr.write('#No_files = '+str(No_files)+'\n')
if No_files==0:
    exit()

for i in range(0, No_rows):
    for j in range(0, No_columns):
        print Sum_List[i][j]/No_files,
    print


sum_files = 0
sum_sqfiles = 0
for f in range(0, No_files):
    values = sum_fileData[f]
    sum_files += values
    sum_sqfiles += values*values

sum_files = sum_files/No_rows
sum_sqfiles = sum_sqfiles/No_rows/No_rows
result = zeros([1, 2*No_columns], float); # this is is make the all the value a float number

for i in range(0, No_columns):
    average = sum_files[i]/No_files
    if No_files == 1:
        variance = 0
    else:
        variance = (sum_sqfiles[i]-No_files*average*average)/(No_files-1) #Bessel correction
        if variance < 0:  #floating point error
            variance = -1.0*variance
    stdErr = 1.3*math.sqrt(variance/No_files) #student's t-distribution
    result[0][2*i] = average
    result[0][2*i+1] = stdErr

print "#Meanvalues and #variance = ",
for j in range(0, len(result[0])):
    print result[0][j],

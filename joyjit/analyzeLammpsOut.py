#! /usr/bin/python

import sys
import os
import numpy
from numpy import *
from math import *

ival    = 0
quiet   = False
zstring = 'Step'

############################################
def readFile(readfile):
    rf = open(readfile)
    data = rf.readlines()
    rf.close()

    i=0
    setnb=0
    rowlist=[]
    while (i <len(data)):
        tmp = data[i].split()
        
        if (len(tmp) > 0 and tmp[0] == zstring):
            setnb += 1
            sys.stderr.write("# set"+str(setnb)+": \n")

            if quiet==False or setnb==1:
                row = "# set "+str(setnb)+":"
                for c in range(len(tmp)):
                    row += str(tmp[c])+' '
                    
                rowlist.append(row)


            cstep=i+1 # locate the step of the current set

            while (cstep < len(data)):
                tmp = data[cstep].split()
                
                if (tmp[0] == 'Loop'):
                    i=cstep
                    break

                row = zeros(len(tmp))
                for c in range(len(tmp)):
                    row[c]=tmp[c]

                rowlist.append(row)
                cstep += 1
                         

        i += 1

    return rowlist


def printData(data):
    print data[0]
    for c in range(len(data[1])):
        print data[1][c],
    print

    if ival==0:
        for r in range(2, len(data)):
            for c in range(len(data[r])):
                print data[r][c],
            print
    else:
        ptime = data[1][0]
        for r in range(2, len(data)):
            
            if data[r][0] == '#' or data[r][0]==ptime or (data[r][0]-ptime)<ival:
                continue

            ptime = data[r][0]
            for c in range(len(data[r])):
                print data[r][c],
            print
                            
    return 0


if len(sys.argv)<2:
    sys.stderr.write("Usage: (i) ifilename \n")
    #for i in range(len(ar)): 
    #    sys.stderr.write(str(i)+" for "+ar[i]+"\n")

    #print 
    exit()

carg = 1
for word in sys.argv[carg:]:
    if word[0] == "-":
        if word == "-ival": # set colorbar boundary for the cg variable
            carg += 1
            ival = float(sys.argv[carg])
            carg += 1
        if word == "-q": # set colorbar boundary for the cg variable
            quiet = True
            carg += 1
        if word == "-zs":
            carg += 1
            zstring = sys.argv[carg]
            sys.stderr.write(zstring+'\n')
            carg += 1
            
        
            
readfile = sys.argv[carg]
carg +=1
#name=ar[int(sys.argv[carg])]
#carg +=1

sys.stderr.write("# reading file "+readfile+"\n")
#sys.stderr.write("# reading parameter "+name+"\n")

if os.path.exists(readfile):
    data=readFile(readfile)
    printData(data)
else:
    print readfile, " does not exist."


            
                



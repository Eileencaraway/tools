from scipy import *
from numpy import *
import sys
import os
import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



if(size(sys.argv)<4) :
    sys.stderr.write('Usage : i.    filename\n')
    sys.stderr.write('Usage : ii.   starting point\n')
    sys.stderr.write('Usage : iii.  ending point\n')
    print
    exit()

carg=1
filename = str(sys.argv[carg])
carg+=1
start = int(sys.argv[carg])
carg+=1
end = int(sys.argv[carg])

X = []
Y = []
Z = []

###########################################################################
# read file

f= open(filename,'r')
count=0

for line in f:
    count+=1
    #&(count%2 ==0)
    if (count > start)&(count<end):

        num=line.split()
        X.append(float(num[1]))
        Y.append(float(num[2]))
        Z.append(float(num[3]))

###########################################################################
# plot 3d scatter
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.plot(X,Y,Z)
#ax.scatter(X,Y,Z)
ax.set_ylabel('X Label')
ax.set_xlabel('Y Label')
ax.set_zlabel('Z Label')

plt.show()

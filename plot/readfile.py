# this python code is used for read data file
#and use the data to plot a 3D picture of particles at that moment
#intend to use for lammps dump file "dumpfile.txt"

import re
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

particlen=list()
xs=list()
ys=list()
zs=list()
particle= open('dumpfile.txt')


for line in particle:
    line = line.rstrip()
    if re.search ('[0-9]+ [0-9]+[.][0-9]+ [0-9]+[.][0-9]+ [0-9]+[.][0-9]+',line):
        print line
        num= line.split()
        particlen.append(float(num[0]))
        xs.append(float(num[1]))
        ys.append(float(num[2]))
        zs.append(float(num[3]))

ax.scatter(xs,ys,zs,s=20, c='r')

ax.set_xlabel('X label')
ax.set_ylabel('Y label')
ax.set_zlabel('Z label')

plt.show()

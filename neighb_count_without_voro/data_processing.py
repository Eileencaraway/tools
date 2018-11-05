from scipy import *
import numpy as np
import matplotlib.pyplot as plt
import re
import glob
import matplotlib.mlab as mlab


total_timestep = 1001
total_id = 3999

filename= []
id =[]
f0 = open('interm_id.dat','r')
count1 = 0
for line in f0:
    num = line.split()
    if count1<total_id:
        id.append(int(num[0]))
        filename.append('track_nneigh_id%d.dat'%int(num[0]))
    count1+=1

tgap =[]

f2 = open('FirstPassageTime.dat','w')
for i in range(total_id):  ## read files
    f1 = open(filename[i],'r')
    data_mat = zeros(total_timestep)
    count = 0
    for line in f1:
        num=line.split()
        data_mat[count]=int(num[1])
        count+=1
    ##print(data_mat)

    f1.close()
    if (data_mat[0]>=10)and(data_mat.min() < 3):
        ind1 = mlab.find(data_mat <=8)
        start=ind1[0]
        ind2 = mlab.find(data_mat <=2)
        end = ind2[0]
        tgap.append(end -start)
        print("id%d start%d end%d tgap%d\n"%(id[i],start,end,end -start))
        f2.write(" %d %d %d %d \n"%(id[i],start,end,end -start))

print(mean(tgap))

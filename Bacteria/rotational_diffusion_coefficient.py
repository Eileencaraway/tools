###this file is for read dumpfile, store information of bacteria position in an array
#store one offset initial point angle of each bacteria
#and use later array to compare with the initial position
#square add up and average over all the bacteria
import re
from scipy import *
import numpy as np
import math
import matplotlib.pyplot as plt

num_bacteria=1000
TIME=3600
t=np.arange(TIME)
MSAD=np.zeros(TIME)
L_bacteria=1.9 # the length of a bacteria
LL=6600 #size of the system
num_atom=3

def read(xxx):
    array=np.zeros((num_atom,num_bacteria,2))
    array_s=np.zeros((num_bacteria,2))
    theta=np.zeros(num_bacteria)
    if(xxx==0):dumpfile=open("dumpfile.0000000000.txt")
    elif((xxx>0)&(xxx<10)):dumpfile=open('dumpfile.0000000%s00.txt'%xxx)
    elif((xxx>=10)&(xxx<100)):dumpfile=open('dumpfile.000000%s00.txt'%xxx)
    elif((xxx>=100)&(xxx<1000)):dumpfile=open('dumpfile.00000%s00.txt'%xxx)
    elif((xxx>=1000)&(xxx<10000)):dumpfile=open('dumpfile.0000%s00.txt'%xxx)
    elif((xxx>=10000)&(xxx<100000)):dumpfile=open('dumpfile.000%s00.txt'%xxx)

    count=0
    for line in dumpfile:
        count+=1
        if(count>=10):
            num = line.split()
            array[(count-10)%num_atom][int((count-10)/num_atom)][0]=num[0]
            array[(count-10)%num_atom][int((count-10)/num_atom)][1]=num[1]

    for i in range(num_bacteria):
        array_s[i][0]=array[num_atom-1][i][0]-array[0][i][0]## should also consider the boundary condition
        if(array_s[i][0]>LL/2):
            array_s[i][0]=LL-array_s[i][0]
        elif(array_s[i][0]<-LL/2):
            array_s[i][0]=LL+array_s[i][0]
        array_s[i][1]=array[num_atom-1][i][1]-array[0][i][1]
        if(array_s[i][1]>LL/2):
            array_s[i][1]=LL-array_s[i][1]
        elif(array_s[i][1]<-LL/2):
            array_s[i][1]=LL+array_s[i][1]

        theta[i]=math.atan2(array_s[i][1],array_s[i][0])

    return theta


def theta_calculate():
    f=open('rotational_diffuision_coefficient.txt','w')
    theta_a=np.zeros((TIME,num_bacteria))
    d_theta=np.zeros(num_bacteria)
    s_theta=np.zeros((num_bacteria))

    for j in range(TIME):
        theta_a[j]=read(5*j)
        #print(theta_a[j])

    for t in range(1,TIME):
        summ=0
        d_theta[:]=0
        for i in range(num_bacteria):
            d_theta[i]=theta_a[t][i]-theta_a[t-1][i]

            if(d_theta[i]>pi):
                d_theta[i]=d_theta[i]-2*pi
            elif(d_theta[i]<-pi):
                d_theta[i]=d_theta[i]+2*pi
            s_theta[i]+=d_theta[i]##add up for different bacteria
            summ+=pow(s_theta[i],2)

        MSAD[t]=summ/num_bacteria

        f.write(str(MSAD[t])+"\n")
    print(MSAD)
    return MSAD

MSAD=theta_calculate()
p,V=np.polyfit(t,MSAD,1)
print(p)
plt.plot(t,MSAD)
plt.plot(t,t*p)
plt.plot(t,t)
plt.title('y=%ft'%p)
plt.xscale('log')
plt.yscale('log')
plt.show()

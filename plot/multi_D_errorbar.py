from scipy import *
import re
from math import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


sample=22500
phi=1
def read(mu,times):
    count=0
    f=open("phi0.%d/mu%s.%d/dumps_mu%s_vf0.%d_tv0.1_tb10/MSD.txt"%(phi,mu,times,mu,phi))
    time=zeros(sample)
    msd=zeros(sample)
    for line in f:
        count+=1
        if (count>1)&(count< sample+1):
            number = line.split()
            time[count-2]=number[0]
            msd[count-2]=number[1]
    return time,msd

msd_all=zeros((9,10,sample))
DD=zeros(9)
D=zeros((9,10))
mu=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
c=['C0','C1','C2']
f2=open('D_0.%d_t1.txt'%phi,'w')
plt.subplot(121)
for n in range(9):
    for i in range(10):
        t,msd_all[n][i]=read(mu[n],i)
        plt.loglog(t,msd_all[n][i],ls='--',label="mu%s"%mu[n])
        def func(x,a):
            return a*x
        popt,pcov=curve_fit(func,t[1000:],msd_all[n][i][1000:])
        #plt.loglog(t[1000:],func(t[1000:],*popt),'b-')


        print(popt)
        D[n][i]=popt/6
        #plt.text(1000, ,'D=%f'%D[i])
    DD[n]=sum(D[n][:])/10
    summ=0
    for i in range(10):
        sq2=(D[n][i]-DD[n])**2
        summ+=sq2
        standard_deviation=sqrt(summ/10)

    f2.write("mu%s %f %f\n"%(mu[n],DD[n], standard_deviation))

plt.xlabel('t')
plt.ylabel('MSD')
##print(D,file=f2)

f2.close()
#plt.legend()


plt.subplot(122)
plt.xlabel('mu')
plt.ylabel('D')
plt.plot(mu,D)
plt.title("D_0.%d_t1"%phi)
plt.savefig('D_0.%d_t1.png'%phi)

from scipy import *
import re
from math import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


sample=22500
phi=5
eq_t=1000000
sim_times=10
mu=0.9
def read(mu,times):
    count=0
    f=open("phi0.%d_eq%d/mu%s_%d/dumps_mu%s_vf0.%d_tv10_tb10/MSD.txt"%(phi,eq_t,mu,times,mu,phi))
    time=zeros(sample)
    msd=zeros(sample)
    for line in f:
        count+=1
        if (count>1)&(count< sample+1):
            number = line.split()
            time[count-2]=number[0]
            msd[count-2]=number[1]
    return time,msd

msd_all=zeros((sim_times,sample))
D=zeros(sim_times)
f2=open('D_0.%d_t1_eq%d.txt'%(phi,eq_t),'w')
plt.subplot(121)

for i in range(sim_times):
    t,msd_all[i]=read(mu,i)
    plt.loglog(t,msd_all[i],ls='--',label="s%s"%i)
    def func(x,a):
        return a*x
    popt,pcov=curve_fit(func,t[1000:],msd_all[i][1000:])
    #plt.loglog(t[1000:],func(t[1000:],*popt),'b-')
    D[i]=popt/6
    print(D[i])
    #plt.text(1000, ,'D=%f'%D[i])

DD=sum(D[:])/sim_times
summ=0
for i in range(sim_times):
    sq2=(D[i]-DD)**2
    summ+=sq2
    standard_deviation=sqrt(summ/sim_times)

f2.write("mu%s %f %f\n"%(mu,DD, standard_deviation))

plt.xlabel('t')
plt.ylabel('MSD')
##print(D,file=f2)

f2.close()
#plt.legend()

xaxis=arange(sim_times)

plt.subplot(122)
plt.xlabel('different simulation')
plt.ylabel('D')
plt.plot(xaxis,D)
plt.title("D_0.%d_t1_eq%d"%(phi,eq_t))
plt.savefig('D_0.%d_t1_eq%d.png'%(phi,eq_t))

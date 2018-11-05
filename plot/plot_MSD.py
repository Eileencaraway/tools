import re
from scipy import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def read(x):
    msd=open('MSD_%d.txt'%x)
    MSD=list()

    for line in msd:
        line=line.rstrip()
        MSD.append(float(line))

    return np.asarray(MSD)

pmsd=np.zeros((10,999))
t=np.arange(999)
c=['C0','C1','C2','C3','C4','C5','C6','C7','C8','C9','C10']
c2=['0.0','0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9','1.0']

for i in range(10):
    pmsd[i]=read(i)
    plt.loglog(t,pmsd[i],c[i],label='t=%ds'%(i))


print(pmsd[5][5:500])
p1=np.polyfit(t[:5],pmsd[5][:5],1)
f1=np.poly1d(p1)
print(p1)
def func(x,a,b):
    return a*x**b
p2,v=curve_fit(func,t[5:100],pmsd[5][5:100],p0=(0.0009,2))
##p2=np.polyfit(t[5:500],pmsd[5][5:500],2)
##f2=np.poly1d(p2)
print(p2)
p3=np.polyfit(t[500:],pmsd[5][500:],1)
f3=np.poly1d(p3)
print(p3)
plt.loglog(t[:5],f1(t[:5]),ls='--')
plt.loglog(t[500:],f3(t[500:]),ls='--')
plt.loglog(t[5:200],p2[0]*t[5:200]**p2[1],ls=':')
plt.text(1.6,0.013,'%f*t'%p1[0])
plt.text(9,1.6,'%fx**%f'%(p2[0],p2[1]))
plt.text(127,15,'%f*t'%p3[0])
plt.show()

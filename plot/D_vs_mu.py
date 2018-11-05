from scipy import *
import re
from math import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def D_vs_mu(phi,equal):
    f=open('D_0.%d_t2_r%d.txt'%(phi,equal))
    mu=zeros(9)
    D=zeros(9)
    error=zeros(9)
    i=0
    for line in f:
        num=line.split()
        mu[i]=num[1]
        D[i]=num[2]
        error[i]=num[3]
        i+=1

    plt.plot(mu,D,label='vf0.%d eq%d'%(phi,equal))
    plt.xlabel('mu')
    plt.ylabel('D')
    plt.title('D_vs_mu')


D_vs_mu(1,10000)
D_vs_mu(2,10000)
D_vs_mu(3,10000)
D_vs_mu(4,10000)
D_vs_mu(5,50000)
D_vs_mu(6,50000)
plt.legend()
plt.savefig('D_vs_mu.png')


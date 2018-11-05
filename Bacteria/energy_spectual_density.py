from scipy import *
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq ## if needed can change to dft?

sample=1800
def read():
    f=('enstrophy.txt','r')
    enstr=zeros(sample)
    count=0
    for line in f:
        num = line.split()
        enstr[count]=num[0]
        count+=1
    return asarray(enstr)

def spectral_density():
    T=18000
    enstr_dot=read()
    sd=rfft(enstr_dot)
    freq=linspace(0,pi/T,1800)

    plt.plot(freq,abs(sp)**2)
    plt.xlabel('frequency')
    plt.ylabel('energy spectral density')
    plt.show()

spectral_density()

from scipy import *
import re
from math import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


sample=22500
phi=6
#equal=60000
def read(mu,times,equal):
    count=0
    f=open("r_phi0.%d/mu%s.%d/dumps_mu%s_vf0.%d_tv0.1_tb10_r%d/MSD.txt"%(phi,mu,times,mu,phi,equal))
    time=zeros(sample)
    msd=zeros(sample)
    for line in f:
        count+=1
        if (count>1)&(count< sample+1):
            number = line.split()
            time[count-2]=number[0]
            msd[count-2]=number[1]
    return time,msd

def MSD_for_diffmu(equal):
    ##initial some array
    msd_all=zeros((9,10,sample))
    sigma=zeros((9,sample))
    msd_t=zeros((9,sample))
    D=zeros(9)   
    mu=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    
    ## open file for prepared to store datas
    f2=open('D_0.%d_t2_r%d.txt'%(phi,equal),'w')
    f3=open('MSD_phi0.%d_r%d.txt'%(phi,equal),'w')

    ## read the msd data from simulation of different mu and different runs
    for n in range(9):
        for i in range(10):
            t,msd_all[n][i]=read(mu[n],i,equal)

    ## get the averaged msd over different runs    
    msd_t=np.sum(msd_all,axis=1)/10

    ## calculate the error bar/sigma of each point in msd
    for n in range(9):
        for j in range(sample):
            summ=0
            for i in range(10):
                sq2=(msd_all[n][i][j]-msd_t[n][j])**2
                summ+=sq2
            sigma[n][j]=sqrt(summ/10)

    ## store the data of msd in a file named with volume fraction and equal time
    for n in range(9):
        for j in range(sample):
            f3.write("%f %f %f\n"%(t[j],msd_t[n][j],sigma[n][j]))
    f3.close()

    fig=plt.figure()
    ax= plt.subplot(111)
    
    ## store the results in f2 how D change with mu 
    print("check if the fit is linear")
    for n in range(9):
        def func(x,a,b):
            return a*x**b
        popt,pcov=curve_fit(func,t[200:sample-1],msd_t[n][200:sample-1],sigma=sigma[n][200:sample-1])

        print(popt)
        D[n]=popt[0]/6
        ax.loglog(t,msd_t[n],ls='-',label="mu%s D%.3e"%(mu[n],D[n]))
        f2.write("mu %s %f %f\n"%(mu[n],D[n],popt[1]))

    ax.set_xlabel('t',fontsize=12)
    ax.set_xlim(left=0.1)
    ax.set_ylabel('MSD',fontsize=12)

    f2.close()
    box = ax.get_position()
    ax.set_position([box.x0,box.y0,box.width*0.6,box.height])
    ax.legend(loc='center left',bbox_to_anchor=(1,0.5))
    plt.title("MSD_0.%d_t2_r%d"%(phi,equal))
    plt.savefig('MSD_0.%d_t2_r%d.png'%(phi,equal))

def DvsMu(equal):
    f4=open('D_0.%d_t2_r%d.txt'%(phi,equal))
    mu=zeros(9)
    D=zeros(9)
    i=0
    for line in f4:
        num=line.split()
        mu[i]=num[1]
        D[i]=num[2]
        i+=1

    plt.plot(mu,D,'-o')
    plt.xlabel('mu')
    plt.ylabel('D')
    plt.title('D_vs_Mu_phi0.%d_r%d'%(phi,equal))
    plt.savefig('D_0.%d_t2_r%d.png'%(phi,equal))

def twoplot(equal):
    ##initial some array
    msd_all=zeros((9,10,sample))
    sigma=zeros((9,sample))
    msd_t=zeros((9,sample))
    D=zeros(9)   
    mu=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
    
    ## open file for prepared to store datas
    f2=open('D_0.%d_t2_r%d.txt'%(phi,equal),'w')
    f3=open('MSD_phi0.%d_r%d.txt'%(phi,equal),'w')

    ## read the msd data from simulation of different mu and different runs
    for n in range(9):
        for i in range(10):
            t,msd_all[n][i]=read(mu[n],i,equal)

    ## get the averaged msd over different runs    
    msd_t=np.sum(msd_all,axis=1)/10

    ## calculate the error bar/sigma of each point in msd
    for n in range(9):
        for j in range(sample):
            summ=0
            for i in range(10):
                sq2=(msd_all[n][i][j]-msd_t[n][j])**2
                summ+=sq2
            sigma[n][j]=sqrt(summ/10)

    ## store the data of msd in a file named with volume fraction and equal time
    for n in range(9):
        for j in range(sample):
            f3.write("%f %f %f\n"%(t[j],msd_t[n][j],sigma[n][j]))
    f3.close()

    fig=plt.figure()
    ax= plt.subplot(221)
    
    ## store the results in f2 how D change with mu 
    print("check if the fit is linear")
    for n in range(9):
        def func(x,a,b):
            return a*x**b
        popt,pcov=curve_fit(func,t[200:sample-1],msd_t[n][200:sample-1],sigma=sigma[n][200:sample-1])

        print(popt)
        D[n]=popt[0]/6
        ax.loglog(t,msd_t[n],ls='-',label="mu%s"%mu[n])
        f2.write("mu %s %f %f\n"%(mu[n],D[n],popt[1]))

    ax.set_xlabel('t',fontsize=12)
    ax.set_xlim(left=0.1)
    ax.set_ylabel('MSD',fontsize=12)

    f2.close()
    #box = ax.get_position()
    #ax.set_position([box.x0,box.y0,box.width*0.6,box.height])
    #ax.legend(loc='center left',bbox_to_anchor=(1,0.5))

    plt.title("MSD_0.%d_r%d"%(phi,equal),fontsize=12)
    #plt.savefig('MSD_0.%d_t2_r%d.png'%(phi,equal))

    ax2= plt.subplot(222)
    ax2.plot(mu,D,'-o')
    ax2.set_xlabel('mu',fontsize=12)
    ax2.set_ylabel('D',fontsize=12)
    plt.title('D_vs_Mu_phi0.%d_r%d'%(phi,equal),fontsize=12)
    #plt.savefig('2plot_MSD_D_0.%d_r%d.png'%(phi,equal))
    
   



def compare_diff_eqtime(mu,equal1,equal2):
    msd1_runs=zeros((10,sample))
    msd2_runs=zeros((10,sample))
    sigma1=zeros(sample)
    sigma2=zeros(sample)
    for i in range(10):
        time,msd1_runs[i]=read(mu,i,equal1)
        time,msd2_runs[i]=read(mu,i,equal2)
    msd1=np.sum(msd1_runs,axis=0)/10
    msd2=np.sum(msd2_runs,axis=0)/10
    
    for j in range(sample):
        summ=0
        for i in range(10):
            sq2=(msd1_runs[i][j]-msd1[j])**2
            summ+=sq2
        sigma1[j]=sqrt(summ/10)

    for j in range(sample):
        summ=0
        for i in range(10):
            sq2=(msd2_runs[i][j]-msd2[j])**2
            summ+=sq2
        sigma2[j]=sqrt(summ/10)

    #plt.loglog(time,msd1,label="equalibrium time %d"%equal1)
    #plt.loglog(time,msd2,label="equalibrium time %d"%equal2)
    #fig=plt.figure()
    ax1=plt.subplot(223)
    ax1.errorbar(time,msd1,yerr=sigma1,label="eq%d"%equal1)
    ax1.errorbar(time,msd2,yerr=sigma2,label="eq%d"%equal2)
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    plt.xlabel('time',fontsize=12)
    plt.ylabel('MSD',fontsize=12)
    plt.title('vf0.%d_mu%f'%(phi,mu),fontsize=12)
    plt.legend(loc=4,fontsize='small')
    plt.savefig('vf0.%d_mu%f.png'%(phi,mu))

def single_msd_time(mu,equal):
    
    msd_runs=zeros((10,sample))
    sigma=zeros(sample)
  
    for i in range(10):
        time,msd_runs[i]=read(mu,i,equal)
    msd=np.sum(msd_runs,axis=0)/10
    
    for j in range(sample):
        summ=0
        for i in range(10):
            sq2=(msd_runs[i][j]-msd[j])**2
            summ+=sq2
        sigma[j]=sqrt(summ/10)

    
    #plt.loglog(time,msd1,label="equalibrium time %d"%equal1)
    #plt.loglog(time,msd2,label="equalibrium time %d"%equal2)
    #fig=plt.figure()
    #ax4=plt.subplot(111)
    ax4=plt.subplot(224)
    #ax1.errorbar(time,msd,yerr=sigma,label="equalibrium time %d"%equal)
    for i in range(10):
        ax4.loglog(time,msd_runs[i])

    ax4.set_xscale("log")
    ax4.set_yscale("log")
    ax4.set_xlabel('time')
    ax4.set_ylabel('MSD',fontsize=12)
    plt.title('vf0.%d  mu%f'%(phi,mu),fontsize=12)
    #plt.legend()
    plt.savefig('allruns_vf0.%d_mu%f_r%d.png'%(phi,mu,equal))


m=[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
#for i in range(9):
    #compare_diff_eqtime(m[i],30000,50000)
    #single_msd_time(m[i],80000)
    #single_msd_time(m[i],100000)
    #print(i)


MSD_for_diffmu(50000)
#DvsMu(80000)
#twoplot(10000)
#compare_diff_eqtime(m[6],10000,10000)
#single_msd_time(m[6],10000)
#plt.subplots_adjust(left=0.123,bottom=0.1,right=0.9,top=0.9,wspace=0.3,hspace=0.33)
#plt.savefig('four_vf0.%d_r%d.png'%(phi,10000))

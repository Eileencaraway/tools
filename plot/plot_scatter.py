from scipy import *
import matplotlib.pyplot as plt
import numpy as np
import sys
from scipy.optimize import curve_fit

if(size(sys.argv)<3):
    sys.stderr.write('Usage : filename1\n')
    sys.stderr.write('Usage : filename2\n')
    exit()
file1 = str(sys.argv[1])
file2 = str(sys.argv[2])
#############################################################################
# read the values from files
def read(string):
    active = []
    phi_c = []
    f0 = open(string,'r')
    for line in f0:
        num = line.split()
        phi_c.append(float(num[0]))
        active.append(float(num[1]))

    return active, phi_c
# fitting with the inverse function and plot the line
def fit_inverse(xdata,ydata):
    def func(x,a,b):
        return (x-a)**2+b
    popt, pcov = curve_fit(func,xdata,ydata,p0=[0.4,0.03])
    #print popt
    x = np.linspace(0.1,0.5,46)
    plt.plot(x,func(x,popt[0],popt[1]))
    plt.xlim(0, 0.6)
    plt.ylim(0,1)

#fiting with poly and plot the line
def fit_poly(xdata,ydata,power):
    # poly
    x = np.linspace(0.1,0.6,21)
    z = np.polyfit(xdata,ydata, power)
    p = np.poly1d(z)
    plt.plot(x,p(x))
    plt.xlim(0.1, 0.6)
    plt.ylim(0,1)

#plot the dots with simulation
def plot_scatter(array):
    f1 = open(file2,'r')
    active = []
    phi = []
    sarle = []
    p = []
    for line in f1:
        num = line.split()
        active.append(float(num[0]))
        phi.append(float(num[1]))
        sarle.append(float(num[2]))
        p.append(float(num[3]))

    plt.scatter(phi,active,s=50,c = p)
    # read from a file
    # x y and a color code
    # three class : phase separated, gas(<0.4), liquid/solid(>0.4 but no ps)
    # use the value of color code to separate
###########################################################################
'''
    ylen = len(active)
    x = np.linspace(0.1,0.6,21)
    y=zeros((ylen,len(x)))
    for i in range(ylen):
        y[i][:]=active[i]
    print(x)

    for i in range(ylen):
        x1 = np.ma.masked_where(x< array[i],x)
        x2 = np.ma.masked_where(x>=array[i],x)
        plt.scatter(x1,y[i],s=100,marker ='d', c='b')
        plt.scatter(x2,y[i],s=100,marker ='o', c ='r')
'''
##########################################################################
active, phi_c_mu= read(file1)
fit_poly(phi_c_mu,active,2)
#fit_inverse(active,phi_c_mu)
plot_scatter(phi_c_mu)
plt.title('Phase Diagram')
plt.xlabel('Density')
plt.ylabel('Pe')
plt.show()

#print("prese enter to continue, now plot the case for no friction")
#active, phi_c= read("crit_mu0.0.dat")
#plt.title('Phase Diagram at mu0.0')

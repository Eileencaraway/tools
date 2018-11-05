from scipy import *
import re
from math import *
import matplotlib.pyplot as plt
import numpy as np
from numpy.fft import fft, fftfreq

num_atom=9
num_bacteria=2601
sample=1800
num_cell=22
L=66
cell_size=L/num_cell
rho=num_bacteria/(L*L)

def read_num_bacteria():
    dump=open("dumps/dumpfile.0000000000.txt")
    count=0
    for line in dump:
        count+=1
        if count==4:
            num_bacteria=int(int(line)/num_atom)
            print("num_bacteria=",num_bacteria)
    return num_bacteria



def read_velocity(xxx):
    if xxx==0:
        dump=open("velocity/v_dumpfile.0000000000.txt")
    elif xxx<10:
        dump=open("velocity/v_dumpfile.000000%d000.txt"%xxx)
    elif xxx<100:
        dump=open("velocity/v_dumpfile.00000%d000.txt"%xxx)
    elif xxx<1000:
        dump=open("velocity/v_dumpfile.0000%d000.txt"%xxx)
    elif xxx<10000:
        dump=open("velocity/v_dumpfile.000%d000.txt"%xxx)
    elif xxx<100000:
        dump=open("velocity/v_dumpfile.00%d000.txt"%xxx)
    elif xxx>=100000:
        print("you files are too big")

    count=0
    array=zeros((num_atom,num_bacteria,2))

    for line in dump:
        count+=1
        if(count>=10):
            num = line.split()
            array[(count-10)%num_atom][int((count-10)/num_atom)][0]=num[0]
            array[(count-10)%num_atom][int((count-10)/num_atom)][1]=num[1]


    return array[int(num_atom/2)][:][:]

def read_position(xxx):
    if xxx==0:
        dump=open("dumps/dumpfile.0000000000.txt")
    elif xxx<10:
        dump=open("dumps/dumpfile.000000%d000.txt"%xxx)
    elif xxx<100:
        dump=open("dumps/dumpfile.00000%d000.txt"%xxx)
    elif xxx<1000:
        dump=open("dumps/dumpfile.0000%d000.txt"%xxx)
    elif xxx<10000:
        dump=open("dumps/dumpfile.000%d000.txt"%xxx)
    elif xxx<100000:
        dump=open("dumps/dumpfile.00%d000.txt"%xxx)
    elif xxx>=100000:
        print("you files are too big")

    count=0
    array=zeros((num_atom,num_bacteria,2))

    for line in dump:
        count+=1
        if(count>=10):
            num = line.split()
            array[(count-10)%num_atom][int((count-10)/num_atom)][0]=num[0]
            array[(count-10)%num_atom][int((count-10)/num_atom)][1]=num[1]


    return array[int(num_atom/2)][:][:]

##print(shape(read_position(1)))
##print(shape(np.concatenate((read_position(1),read_velocity(1)),axis=1)))




## separate the box into 22*5 part
## for the particle fall into the box, sum up the velocity
## this is the coarse graining process
def coarse_grain(x):
    particles=zeros((num_bacteria,4))
    particles=np.concatenate((read_position(x),read_velocity(x)),axis=1)
    cell=zeros((num_cell,num_cell,5))
    curl=zeros((num_cell-2,num_cell-2))
    for i in range(num_bacteria):
        cx=int(particles[i][0]/cell_size)
        if cx==22:
            cx=22-1
        cy=int(particles[i][1]/cell_size)
        if cy==22:
            cy=22-1
        cell[cx][cy][0]=cell_size*cx+cell_size/2.0
        cell[cx][cy][1]=cell_size*cy+cell_size/2.0
        cell[cx][cy][2]+=particles[i][2]## for recording the vx
        cell[cx][cy][3]+=particles[i][3]## for recording the vy
        cell[cx][cy][4]+=1## this is for recording the n of particle in the box
    f=open('velocity_field.txt','w')
    for i in range(num_cell):
        for j in range(num_cell):
            if cell[i][j][4]!=0:
                cell[i][j][2]=cell[i][j][2]/cell[i][j][4] ## now it is the average velocity in the grid
                cell[i][j][3]=cell[i][j][3]/cell[i][j][4]

            print('%d  %d %f %f\n'%(i,j,cell[i][j][2],cell[i][j][3]),file=f)

## this function is for calculation the vorticity
    f2=open('curl_field.txt','w')
    for i in range(num_cell-2):
        for j in range(num_cell-2):
            curl[i][j]=(cell[i+2][j][3]-cell[i][j][3])/2-(cell[i][j+2][2]-cell[i][j][2])/2

            print('%d  %d %f\n'%(i,j,curl[i][j]),file=f2)


    enstrophy= 0.5*(sum(curl[:][:]**2))/(num_cell-2)**2
    print(enstrophy)
    return enstrophy

num_bacteria=read_num_bacteria()
f3=open('enstrophy.txt','w')
ens=zeros(sample)
## for now y cannot smaller than 10
for i in range(sample):
    ens[i]=coarse_grain(i)
    print(ens[i],file=f3)


print("result=",sum(ens[50:])/(sample-50))



def spectral_density():
    T=sample*10
    enstr_dot=ens
    ps=abs(fft(enstr_dot))**2
    freqs=fftfreq(sample,10)
    idx=argsort(freqs)

    plt.plot(freqs[idx],ps[idx])
    plt.xlabel('frequency')
    plt.ylabel('energy spectral density')
    plt.show()

spectral_density()

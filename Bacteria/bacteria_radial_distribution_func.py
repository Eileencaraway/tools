from scipy import *
import re
from math import *
import matplotlib.pyplot as plt

num_atom=3
num_bacteria=7176
particles=zeros((num_bacteria,2))

L=66
rho=num_bacteria/(L*L)
nbins=500
g=zeros(nbins)


def read(xxx):
    dump=open("dumpfile.000%d00.txt"%xxx)
    count=0
    array=zeros((num_atom,num_bacteria,2))

    for line in dump:
        count+=1
        if(count>=10):
            num = line.split()
            array[(count-10)%num_atom][int((count-10)/num_atom)][0]=num[0]
            array[(count-10)%num_atom][int((count-10)/num_atom)][1]=num[1]


    return array[int(num_atom/2)][:][:]

##switch=0 initialize switch=1 sample switch=2 result
def gr(switch):
    global ngr,bin_size,nbins,g
    if(switch==0):
        ngr=0
        print("ngr is initialized")
        bin_size=L/(2*nbins)
        for i in range(nbins):
            g[i]=0

    elif(switch==1):
        ngr+=1  ## ngr number of times to calculate gr
        for i in range(num_bacteria-1):
            for j in range(i+1,num_bacteria):
                dx=particles[i][0]-particles[j][0]
                dy=particles[i][1]-particles[j][1]
                #print(dx)
                dx -=  L*round(dx/L)
                dy -=  L*round(dy/L) ## L is the size of the box at x and at y
                r2 = dx*dx + dy*dy
                if(r2<L*L/4):
                    #print(r2)
                    r = sqrt(r2)
                    ig = int(r/bin_size)
                    g[ig]+=1
                #print(gr)

    elif((switch==2)&(ngr!=0)):
        outfile=open('RDF.dat','w')
        radius=zeros(nbins)
        for i in range(nbins):
            radius[i] = (i+0.5)*bin_size;
            area = pi*bin_size*bin_size*((i+1)*(i+1)-(i)*(i))*rho
            #print(g[i])
            #g[i]=g[i]/area
            g[i] = 2*g[i]/(ngr*area*num_bacteria)
            #print(g[i])
            outfile.write(str(radius[i])+" "+str(g[i])+"\n")

        plt.plot(radius,g)
        plt.show()
        outfile.close()

gr(0)
particles=read(53900)
gr(1)
gr(2)

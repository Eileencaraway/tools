import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# read arguements
###################################################################################
dt      = 0.00004
verbose = False
COM     = False
dim     = 3

###################################################################################
if(size(sys.argv)<1):
    sys.stderr.write('Usage : i. timescale \n')
    exit()

carg = 1
for word in sys.argv[carg:]:
    if word[0] == "-":
        if word == "-dt":
            carg += 1
            dt = float(sys.argv[carg])
            carg += 1
        if word == "-dim":
            carg += 1
            dim = int(sys.argv[carg])
            carg += 1
        if word == "-com":
            carg += 1
            COM   = True
        if word == "-verb":
            carg += 1
            verbose = True


timescale = int(sys.argv[carg])
carg += 1

#####
#init
tsrt = 'dumpfile.'+str(timescale).zfill(10)+'.txt'
init = LammpsOperations()
init.readFile3d(tsrt, verbose)
L       = init.cell[1]
num_particle =init.nb_atoms

# core algorithms to calculate Dr for each particles
def onefile(tsrt,tend):

    # select snap ids corresponding to timesteps
    if os.path.exists(tsrt)&os.path.exists(tend):
        if dim==3:
            lstr  = LammpsOperations()
            lstr.readFile3d(tsrt, verbose)
            lend  = LammpsOperations()
            lend.readFile3d(tend, verbose)
        else:
            lstr  = LammpsOperations()
            lstr.readFile(tsrt, verbose)
            lend  = LammpsOperations()
            lend.readFile(tend, verbose)
        ts0     = lstr.tsteps
        ts1     = lend.tsteps
        dts     = (ts1-ts0)*dt

    else:
        print tsrt, " does not exist. or", tend, " does not exist. "

    omega2 = zeros(num_particle)
    for i in range(num_particle):
        omega2[i] = lstr.omegax[i]*lend.omegax[i]+lstr.omegay[i]*lend.omegay[i]+ lstr.omegaz[i]*lend.omegaz[i]
    avg_omega = mean(omega2)

    return avg_omega


### only calculate one point
def avg_files(time):
    omega = zeros(999)
    for i in range(999):
        tsrt = 'dumpfile.'+str(time*(i+1)).zfill(10)+'.txt'
        tend = 'dumpfile.'+str(time*(i+2)).zfill(10)+'.txt'
        print(tend)
        omega[i] =onefile(tsrt,tend)
    return mean(omega)


## calculate several points
t_list =[0,1,2,3,4,5,6,7,8,9,10]
omega_list = zeros(len(t_list))
f = open('corr_omega.txt','w')
for i in range(len(t_list)):
    if t_list[i] == 0:
        t0 = 'dumpfile.0000000000.txt'
        omega_list[i]= onefile(t0,t0)
    else:
        omega_list[i] = avg_files(t_list[i]*timescale)
    f.write("%1.6f %1.6f \n"%(t_list[i]*dt*timescale, omega_list[i]))

f.close()

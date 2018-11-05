import sys
import os
import StringIO
from numpy import *
from lammpsOperationsnp import *
from scipy import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
########
# read arguements
###################################################################################
dt      = 0.00004
verbose = False
COM     = False
dim     = 3

###################################################################################
if(size(sys.argv)<2):
    sys.stderr.write('Usage : i. timescale \n')
    sys.stderr.write('        ii. bin number \n')
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
nbin = int(sys.argv[carg])
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

    dxu = zeros(num_particle)
    dyu = zeros(num_particle)
    dzu = zeros(num_particle)
    dru = zeros(num_particle)
    thetax = zeros(num_particle)
    thetay = zeros(num_particle)
    thetaz = zeros(num_particle)
    theta  = zeros(num_particle)
    r2     = zeros(num_particle)
    Dr     = zeros(num_particle)
    D      = zeros(num_particle)

    for i in range(num_particle):
        dxu[i]    = lstr.xu[i]-lend.xu[i]
        dyu[i]    = lstr.yu[i]-lend.yu[i]
        thetax[i] = lend.dirx[i] - lstr.dirx[i]
        thetay[i] = lend.diry[i] - lstr.diry[i]
        if dim ==2:
            theta[i]  = thetax[i]*thetax[i] + thetay[i]*thetay[i]
            r2[i]     = dxu[i]*dxu[i]+dyu[i]*dyu[i]
            Dr[i]     = theta[i]/(4*dts)
            D[i]      = r2[i]/(4*dts)
        elif dim==3:
            dzu[i]    = lstr.zu[i]-lend.zu[i]
            thetaz[i] = lend.dirz[i] - lstr.dirz[i]
            theta[i]  = thetax[i]*thetax[i] + thetay[i]*thetay[i] + thetaz[i]*thetaz[i]
            r2[i]     = dxu[i]*dxu[i]+dyu[i]*dyu[i]+dzu[i]*dzu[i]
            Dr[i]     = theta[i]/(6*dts)
            D[i]      = r2[i]/(6*dts)

    return Dr,D

#######
# average
# the problem is choice time scale (at least do 8 average is better than no )
Dr = zeros((8,num_particle))
D  = zeros((8,num_particle))
for i in range(8):
    sdumpf = 'dumpfile.'+str(timescale*(i+1)).zfill(10)+'.txt'
    edumpf = 'dumpfile.'+str(timescale*(i+2)).zfill(10)+'.txt'
    Dr[i],D[i] = onefile(sdumpf,edumpf)

Avg_Dr = mean(Dr,axis=0)
Avg_D  = mean(D,axis=0)
time = timescale*dt
#####
# bining and plot
ndr, dr_bins, dr_patches= plt.hist(Avg_Dr, bins=nbin, range=(0.0,0.006))
binsize = dr_bins[1]-dr_bins[0]
A = sum(ndr)*binsize
for i in range(len(ndr)):
    ndr[i]= ndr[i]/A
plt.xlabel("magnitude of Dr")
plt.ylabel("num_of_particles")
plt.title("%1.4f"%time)
plt.savefig('Dr_distribution_%1.4f.png'%time)

f= open('Dr_bin_dist_%1.4f.txt'%time,'w')
for i in range(len(ndr)):
    f.write('%1.6f %1.6f \n'%(dr_bins[i]+binsize/2,ndr[i]))
f.close()


# bin of MSD
nd, d_bins, d_patches= plt.hist(Avg_D, bins=nbin, range=(D.min(),D.max()))
binsize = d_bins[1]-d_bins[0]
A = sum(nd)*binsize
for i in range(len(nd)):
    nd[i]= nd[i]/A
plt.xlabel("magnitude of D")
plt.ylabel("num_of_particles")
plt.title("%1.4f"%time)
plt.savefig('D_distribution_%1.4f.png'%time)

f1= open('D_bin_dist_%1.4f.txt'%time,'w')

for i in range(len(nd)):
    f1.write('%1.6f %1.6f \n'%(d_bins[i]+binsize/2,nd[i]))
f1.close()

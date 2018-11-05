from scipy import *
from scipy import interpolate
from numpy import *
import os
import sys
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
###############################################################
if size(sys.argv)<2:
    sys.stderr.write("Usage: bin size ")
    print
    sys.exit()

density_list = [0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6]
nx = len(density_list)  # read from command line
ny = int(sys.argv[1]) #100
z = zeros((nx,ny+1)) #11*101
############################################################
for i in range(nx):
    val= []
    f = open('ld-phi%s-mu0.0-N10000.txt'%density_list[i])
    for line in f:
        num = line.split()
        if len(num) < 2:
            continue  # break out from the loop and do not run the following
        val.append(float(num[1]))
    #print(len(val))
    z[i][:-1] = asarray(val)
#z= transpose(z)
print(z)
z=z.T
#z=log(z*100+0.1)  # rescale value Z
x = asarray(density_list)
#print(len(x))
y = linspace(0.0,1.00,ny+1)

X,Y = meshgrid(x,y)
##################################################################
# the third trial, manually get the values
xnew = linspace(0.1,0.6,21)
ynew = y
Xnew,Ynew =meshgrid(xnew,ynew)
znew = zeros((len(ynew),len(xnew)))
#for i in range(nx):
#    znew[i*2]=z[i]

#for i in range(nx-1):
#    znew[i*2+1]= (z[i]+z[i+1])/2
for i in range(ny-1):
    f = interpolate.interp1d(x,z[i],kind='linear')
    znew[i][:]=f(xnew)
##################################################################
#def func(ix,iy):
#    return z[x.index(ix)][y.index(iy)]
###################################################################
# second trial, also didn't get desired results
#grid_x,grid_y= mgrid[amin(x):amax(x):21j,amin(y):amax(y):101j] # here define the values on x, y
#print(grid_x)
#points = zeros((nx*ny,2)) # this is the coordinates, but not value
#values = zeros(nx*ny)
#for i in range(nx):
#    for j in range(ny):
#        points[i*ny+j][0]=i
#        points[i*ny+j][1]=j
#        values[i*ny+j]=z[i][j] # this is a nx * ny shape
#grid_z=interpolate.griddata(points,values,(grid_x,grid_y),method='nearest')
#########################################################################
# first trial, don't get desired results
#dx, dy = 0.1, 0.01
#X,Y = np.meshgrid[slice(0.0,1,dy),slice(0.1,0.7,dx)]
#xnew,ynew = np.mgrid[0.1:0.6:21j,0:1:101j]
#tck = interpolate.bisplrep(X,Y,z)
#znew = interpolate.bisplev(xnew[:,0],ynew[0,:],tck)
#########################################################################
####pick desired colormap
#znew=log(znew*100+0.1)

levels = MaxNLocator(nbins=50).tick_values(znew.min(),znew.max())
cmap = plt.get_cmap('jet')
norm = BoundaryNorm(levels,ncolors= cmap.N, clip = True) #,
plt.pcolormesh(Xnew,Ynew,znew,cmap = cmap, norm = norm)
#plt.imshow(z.T,extent=(amin(x),amax(x),amin(y),amax(y)),origin='lower',cmap = cmap, norm = norm)
plt.savefig('ld-mu0.0.png')

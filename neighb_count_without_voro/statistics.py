# this file is for doing statistic of any kind of data
# the output of this can be a deviation, mean, skew and kurtosis, etc
from scipy import *
from numpy import *
import scipy.stats
import sys
## read the file name and the col of the data(if > 2 column in the file)
if(len(sys.argv)<2):
    sys.stderr.write('Usage : i. filename\n')
    sys.stderr.write('        ii. col \n')
    exit()
##sys.argv first argv is the python file, if you want to
##input the filename, filename is the 2rd argv
carg = 1
file  = str(sys.argv[carg])
carg += 1
col = int(sys.argv[carg])
########################################################
# a function that is really read the file and store the values in a array
def readfile(file):

    f = open(file,'r')
    # read the first colunms and the second columns
    col1 =[]
    for line in f:
        num = line.split()
        col1.append(int(num[col]))  # id of the particles
    #col_matrix = np.array([col1,col2])
    #print(col_matrix)
    return col1
#######################################################
ncluster = readfile(file)
# do some statistic on the array and output both to file and on screen
def analysis(array):
    n_array = len(array)
    deviation= std(array) #std = sqrt(mean(abs(x - x.mean())**2))
    #skew = scipy.stats.skew(array)
    #kurtosis = scipy.stats.kurtosis(array)
    #sarle = (skew**2+1)/(kurtosis+3*(n_array-1)**2/((n_array-2)*(n_array-3)))
    print("deviation=%1.4f"%deviation)
    #print("skew=%1.2f"%skew)
    #print("kurtosis=%1.2f"%kurtosis)
    #print("sarle=%1.2f"%sarle)
    fout = open('ncluster_dev_vp.dat','a')

analysis(ncluster)

import sys
import os
import numpy
from numpy import *
from math import *
import struct

class LammpsOperations:

    def __init__(self):
        self.header=''
        self.nb_atoms=0
        self.tsteps  =0
        self.cell =[]
        self.xy   =0
        self.rad  =[]
        self.x    =[]
        self.y    =[]
        self.z    =[]
        self.ix   =[]
        self.iy   =[]
        self.iz   =[]
        self.xu   =[]
        self.yu   =[]
        self.zu   =[]
        self.vx   =[]
        self.vy   =[]
        self.vz   =[]

        self.directorx = []
        self.directory = []
        self.directorz = []

        self.omegax  =[]
        self.omegay  =[]
        self.omegaz  =[]

        self.ADx  =[]
        self.ADy  =[]
        self.ADz  =[]

        self.q1   =[]
        self.q2   =[]
        self.q3   =[]
        self.q4   =[]

        self.nb_entries=0
        self.p1   =[]
        self.p2   =[]
        self.p3   =[]
        self.p4   =[]
        self.p5   =[]
        self.p6   =[]
        self.p7   =[]
        self.p8   =[]
        self.p9   =[]
        self.p10  =[]
        self.p11  =[]
        self.p12  =[]
        self.p13  =[]
        self.p14  =[]
        self.p15  =[]

        self.writeBin=False

    def initialize(self):
        self.cell=[]
        self.rad = [0 for i in range(self.nb_atoms)]
        self.x   = [0 for i in range(self.nb_atoms)]
        self.y   = [0 for i in range(self.nb_atoms)]
        self.z   = [0 for i in range(self.nb_atoms)]
        self.xu  = [0 for i in range(self.nb_atoms)]
        self.yu  = [0 for i in range(self.nb_atoms)]
        self.zu  = [0 for i in range(self.nb_atoms)]
        self.omegax  = [0 for i in range(self.nb_atoms)]
        self.omegay  = [0 for i in range(self.nb_atoms)]
        self.omegaz  = [0 for i in range(self.nb_atoms)]
        self.ADx  = [0 for i in range(self.nb_atoms)]
        self.ADy  = [0 for i in range(self.nb_atoms)]
        self.ADz  = [0 for i in range(self.nb_atoms)]
        #self.directorx = [0 for i in range(self.nb_atoms)]
        #self.directory = [0 for i in range(self.nb_atoms)]
        #self.directorz = [0 for i in range(self.nb_atoms)]

        return 0


    def initializePairs(self):
        self.cell=[]
        self.p1  = [0 for i in range(self.nb_entries)]
        self.p2  = [0 for i in range(self.nb_entries)]
        self.p3  = [0 for i in range(self.nb_entries)]
        self.p4  = [0 for i in range(self.nb_entries)]
        self.p5  = [0 for i in range(self.nb_entries)]
        self.p6  = [0 for i in range(self.nb_entries)]
        self.p7  = [0 for i in range(self.nb_entries)]
        self.p8  = [0 for i in range(self.nb_entries)]
        self.p9  = [0 for i in range(self.nb_entries)]
        self.p10 = [0 for i in range(self.nb_entries)]
        self.p11 = [0 for i in range(self.nb_entries)]
        self.p12 = [0 for i in range(self.nb_entries)]
        self.p13 = [0 for i in range(self.nb_entries)]
        self.p14 = [0 for i in range(self.nb_entries)]
        self.p15 = [0 for i in range(self.nb_entries)]
        return 0


    def readFile3d(self, readfile, verbose=False):

        for line in open(readfile):
            tmp = line.split()

            if tmp[0]=="ITEM:" and tmp[1]=="TIMESTEP":
                cline=0
                  # current line number of the required snap
            cline += 1

            if cline==2:
                self.tsteps = int(tmp[0])
                if verbose:
                    sys.stderr.write("# found timestep "+str(self.tsteps)+"\n")

            if cline==4:
                self.nb_atoms = int(tmp[0])
                self.initialize()
                if verbose:
                    sys.stderr.write("# found "+str(self.nb_atoms)+" atoms\n")

            if cline>5 and cline<9:
                self.cell.append(float(tmp[0]))
                self.cell.append(float(tmp[1]))
                if cline==6 and len(tmp)==3:
                    self.xy = float(tmp[2])

            if cline==8 and verbose:
                    sys.stderr.write("# Dimension of the box:"+str(self.cell)+"\n")

            if cline==9:
                self.header=line
                if len(tmp)>13 and len(tmp)!= 16:
                    sys.stderr.write("!!! Warning !!!\n")
                    sys.stderr.write("read first 13 values out of "+str(len(tmp)-2)+"\n")
                if verbose:
                    sys.stderr.write(self.header+"\n")

            if cline > 9:
                id              = int(tmp[0])-1
                self.x[id]      = float(tmp[1])
                self.y[id]      = float(tmp[2])
                self.z[id]      = float(tmp[3])
                self.xu[id]     = float(tmp[4])
                self.yu[id]     = float(tmp[5])
                self.zu[id]     = float(tmp[6])
                self.omegax[id] = float(tmp[7])
                self.omegay[id] = float(tmp[8])
                self.omegaz[id] = float(tmp[9])
                self.rad[id]    = float(tmp[10])

                #self.directorx[id] = float(tmp[14])
                #self.directory[id] = float(tmp[15])
                #self.directorz[id] = float(tmp[16])

                if len(tmp) > 11:
                    self.ADx[id]    = float(tmp[11])
                    self.ADy[id]    = float(tmp[12])
                    self.ADz[id]    = float(tmp[13])
                """
                self.q1[id]  = float(tmp[8])
                self.q2[id]  = float(tmp[9])
                self.q3[id]  = float(tmp[10])
                self.q4[id]  = float(tmp[11])

            if cline > 9:
                id              = int(tmp[10])-1

                self.x[id]      = float(tmp[0])
                self.y[id]      = float(tmp[1])
                self.z[id]      = float(tmp[2])
                #self.xu[id]     = float(tmp[4])
                #self.yu[id]     = float(tmp[5])
                #self.zu[id]     = float(tmp[6])
                self.omegax[id] = float(tmp[3])
                self.omegay[id] = float(tmp[4])
                self.omegaz[id] = float(tmp[5])
                self.rad[id]    = float(tmp[9])


                if len(tmp) > 11:
                    self.vx[id]  = float(tmp[11])
                    self.vy[id]  = float(tmp[12])
            """
            if cline==(9+self.nb_atoms):
                break

        return 0

    def readFile(self, readfile, verbose=False):

        for line in open(readfile):
            tmp = line.split()

            if tmp[0]=="ITEM:" and tmp[1]=="TIMESTEP":
                cline=0
                  # current line number of the required snap
            cline += 1

            if cline==2:
                self.tsteps = int(tmp[0])
                if verbose:
                    sys.stderr.write("# found timestep "+str(self.tsteps)+"\n")

            if cline==4:
                self.nb_atoms = int(tmp[0])
                self.initialize()
                if verbose:
                    sys.stderr.write("# found "+str(self.nb_atoms)+" atoms\n")

            if cline>5 and cline<9:
                self.cell.append(float(tmp[0]))
                self.cell.append(float(tmp[1]))
                if cline==6 and len(tmp)==3:
                    self.xy = float(tmp[2])

            if cline==8 and verbose:
                    sys.stderr.write("# Dimension of the box:"+str(self.cell)+"\n")

            if cline==9:
                self.header=line
                if len(tmp)>7 and len(tmp)!=8:
                    sys.stderr.write("!!! Warning !!!\n")
                    sys.stderr.write("read first 7 values out of "+str(len(tmp)-2)+"\n")
                if verbose:
                    sys.stderr.write(self.header+"\n")

            if cline > 9:
                id              = int(tmp[0])-1
                self.x[id]      = float(tmp[1])
                self.y[id]      = float(tmp[2])
                self.xu[id]     = float(tmp[3])
                self.yu[id]     = float(tmp[4])
                self.omegaz[id] = float(tmp[5])
                self.rad[id]    = float(tmp[6])

                if len(tmp) > 7:
                    self.ADz[id]  = float(tmp[7])
                """
                self.q1[id]  = float(tmp[8])
                self.q2[id]  = float(tmp[9])
                self.q3[id]  = float(tmp[10])
                self.q4[id]  = float(tmp[11])
                """


            if cline==(9+self.nb_atoms):
                break

        return 0

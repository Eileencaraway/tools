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
        self.ix   =[]
        self.iy   =[]
        self.vx   =[]
        self.vy   =[]
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

        self.columns = zeros([1,1])
        self.writeBin=False


    def initialize(self):
        self.cell=[]
        self.rad = [0 for i in range(self.nb_atoms)]
        self.x   = [0 for i in range(self.nb_atoms)]
        self.y   = [0 for i in range(self.nb_atoms)]
        self.ix  = [0 for i in range(self.nb_atoms)]
        self.iy  = [0 for i in range(self.nb_atoms)]
        self.vx  = [0 for i in range(self.nb_atoms)]
        self.vy  = [0 for i in range(self.nb_atoms)]
        self.q1  = [0 for i in range(self.nb_atoms)]
        self.q2  = [0 for i in range(self.nb_atoms)]
        self.q3  = [0 for i in range(self.nb_atoms)]
        self.q4  = [0 for i in range(self.nb_atoms)]
        
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

    
    def readFile(self, readfile, rsnap, verbose=False):
        csnap=-1 # current snap number
        
        for line in open(readfile):
            tmp = line.split()
            
            if tmp[0]=="ITEM:" and tmp[1]=="TIMESTEP":
                cline=0  # current line number of the required snap
                csnap += 1
            
            if csnap==rsnap or rsnap<0:
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
                    if len(tmp)>8 and len(tmp)!=10:
                        sys.stderr.write("!!! Warning !!!\n")
                        sys.stderr.write("read first 8 values out of "+str(len(tmp)-2)+"\n") 
                    if verbose:
                        sys.stderr.write(self.header+"\n")

                if cline > 9:
                    id           = int(tmp[0])-1
                    self.x[id]   = float(tmp[1])
                    self.y[id]   = float(tmp[2])
                    self.ix[id]  = int(tmp[3])
                    self.iy[id]  = int(tmp[4])
                    self.rad[id] = float(tmp[5])

                    if len(tmp) > 6:
                        self.vx[id]  = float(tmp[6])
                        self.vy[id]  = float(tmp[7])
                    """
                    self.q1[id]  = float(tmp[8])
                    self.q2[id]  = float(tmp[9])
                    self.q3[id]  = float(tmp[10])
                    self.q4[id]  = float(tmp[11])                        
                    """
                    
                        
            if cline==(9+self.nb_atoms):
                if self.writeBin:
                    self.writeBinFile(readfile)
                if rsnap >= 0: 
                    break

        return 0


    def readPairFile(self, readfile, rsnap, verbose=False):
        csnap=-1 # current snap number
        
        for line in open(readfile):
            tmp = line.split()
            
            if tmp[0]=="ITEM:" and tmp[1]=="TIMESTEP":
                cline=0  # current line number of the required snap
                csnap += 1
            
            if csnap==rsnap or rsnap<0:
                cline += 1

                if cline==2:
                    self.tsteps = int(tmp[0])
                    if verbose:
                        sys.stderr.write("# found timestep "+str(self.tsteps)+"\n")
            
                if cline==4:
                    self.nb_entries = int(tmp[0])
                    self.initializePairs()
                    if verbose:
                        sys.stderr.write("# found "+str(self.nb_entries)+" entries\n")
                    
                if cline>5 and cline<9:
                    self.cell.append(float(tmp[0]))
                    self.cell.append(float(tmp[1]))
                if cline==8 and verbose:
                        sys.stderr.write("# Dimension of the box:"+str(self.cell)+"\n")

                if cline==9:
                    self.header=line
                    if len(tmp)!=18:
                        sys.stderr.write("!!! Warning !!!\n")
                        sys.stderr.write("expecting 16 values, got "+str(len(tmp)-2)+"\n") 
                    if verbose:
                        sys.stderr.write(self.header+"\n")

                if cline > 9:
                    id            = int(tmp[0])-1
                    self.p1[id]   = int(tmp[1])
                    self.p2[id]   = int(tmp[2])
                    self.p3[id]   = float(tmp[3])
                    self.p4[id]   = float(tmp[4])
                    self.p5[id]   = float(tmp[5])
                    self.p6[id]   = int(tmp[6])
                    self.p7[id]   = float(tmp[7])
                    self.p8[id]   = float(tmp[8])
                    self.p9[id]   = float(tmp[9])
                    self.p10[id]  = float(tmp[10])
                    self.p11[id]  = float(tmp[11])
                    self.p12[id]  = float(tmp[12])
                    self.p13[id]  = float(tmp[13])
                    self.p14[id]  = float(tmp[14])
                    self.p15[id]  = float(tmp[15])


            if cline==(9+self.nb_entries):
                if self.writeBin:
                    self.writeBinPairFile(readfile)
                if rsnap >= 0: 
                    break

        return 0
    
    def readSelectedColumns(self, readfile, rsnap, colist, verbose=False):
        csnap=-1 # current snap number

        for line in open(readfile):
            tmp = line.split()
            
            if tmp[0]=="ITEM:" and tmp[1]=="TIMESTEP":
                cline=0  # current line number of the required snap
                csnap += 1
            
            if csnap==rsnap or rsnap<0:
                cline += 1

                if cline==2:
                    self.tsteps = int(tmp[0])
                    if verbose:
                        sys.stderr.write("# found timestep "+str(self.tsteps)+"\n")
            
                if cline==4:
                    self.nb_atoms = int(tmp[0])
                    self.columns  = zeros([len(colist), self.nb_atoms])
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
                    if verbose:
                        sys.stderr.write(self.header+"\n")

                if cline > 9:
                    id   = int(tmp[0])-1
                    for coi in range(len(colist)):
                        self.columns[coi][id] = float(tmp[colist[coi]])     
                        
            if cline==(9+self.nb_atoms):
                if self.writeBin:
                    self.writeBinFile(readfile)
                if rsnap >= 0: 
                    break

        return 0

        
    def selectReadFile(self, readfile, rsnap, ftype, verbose=False):
        if ftype=="position":
            self.readFile(readfile, rsnap, verbose)
        if ftype=="pair":
            self.readPairFile(readfile, rsnap, verbose)

        return 0


    def readBinFile(self, readfile, verbose=False):
        rf            = open(readfile,'rb')
        self.tsteps   = int(fromfile(rf, 'int32', 1))
        self.nb_atoms = int(fromfile(rf, 'int32', 1))
        self.initialize()
        for d in range(6):
            self.cell.append(float(fromfile(rf, 'float32', 1)))
        self.header=rf.readline()
        header_items=len(self.header.split())
        if verbose:
            sys.stderr.write("# found timestep "+str(self.tsteps)+"\n")
            sys.stderr.write("# found "+str(self.nb_atoms)+" atoms\n")
            sys.stderr.write("# Dimension of the box:"+str(self.cell)+"\n")
            sys.stderr.write(self.header+"\n")

        for i in range(self.nb_atoms):
            id           = int(fromfile(rf, 'int32', 1))-1
            self.x[id]   = float(fromfile(rf, 'float32', 1))
            self.y[id]   = float(fromfile(rf, 'float32', 1))
            self.ix[id]  = int(fromfile(rf, 'int32', 1)) 
            self.iy[id]  = int(fromfile(rf, 'int32', 1)) 
            self.rad[id] = float(fromfile(rf, 'float32', 1))
            if header_items > 8:
                self.vx[id]  = float(fromfile(rf, 'float32', 1))
                self.vy[id]  = float(fromfile(rf, 'float32', 1))
            
        rf.close()
        return 0


    def readBinPairFile(self, readfile, verbose=False):
        rf              = open(readfile,'rb')
        self.tsteps     = int(fromfile(rf, 'int32', 1))
        self.nb_entries = int(fromfile(rf, 'int32', 1))
        self.initializePairs()
        for d in range(6):
            self.cell.append(float(fromfile(rf, 'float32', 1)))
        self.header=rf.readline()
        if verbose:
            sys.stderr.write("# found timestep "+str(self.tsteps)+"\n")
            sys.stderr.write("# found "+str(self.nb_entries)+" entries\n")
            sys.stderr.write("# Dimension of the box:"+str(self.cell)+"\n")
            sys.stderr.write(self.header+"\n")

        for i in range(self.nb_entries):
            id           = int(fromfile(rf, 'int32', 1))-1
            self.p1[id]  = int(fromfile(rf, 'int32', 1))
            self.p2[id]  = int(fromfile(rf, 'int32', 1))
            self.p3[id]  = float(fromfile(rf, 'float32', 1))
            self.p4[id]  = float(fromfile(rf, 'float32', 1))
            self.p5[id]  = float(fromfile(rf, 'float32', 1))
            self.p6[id]  = int(fromfile(rf, 'int32', 1))
            self.p7[id]  = float(fromfile(rf, 'float32', 1))
            self.p8[id]  = float(fromfile(rf, 'float32', 1))
            self.p9[id]  = float(fromfile(rf, 'float32', 1))
            self.p10[id] = float(fromfile(rf, 'float32', 1))
            self.p11[id] = float(fromfile(rf, 'float32', 1))
            self.p12[id] = float(fromfile(rf, 'float32', 1))
            self.p13[id] = float(fromfile(rf, 'float32', 1))
            self.p14[id] = float(fromfile(rf, 'float32', 1))
            self.p15[id] = float(fromfile(rf, 'float32', 1))
        
        rf.close()
        return 0


    def selectReadBinFile(self, readfile, ftype, verbose=False):
        if ftype=="position":
            self.readBinFile(readfile, verbose)
        if ftype=="pair":
            self.readBinPairFile(readfile, verbose)

        return 0

    
    def writeBinFile(self, readfile):
        wfilename = readfile+'-ts-'+str(self.tsteps)+'.bin' 
        sys.stderr.write("## writing "+wfilename+"\n")
        writefile = open(wfilename,'wb')
        writefile.write(struct.pack('i', self.tsteps))
        writefile.write(struct.pack('i', self.nb_atoms))
        for d in range(3):
            writefile.write(struct.pack('f', self.cell[2*d]))
            writefile.write(struct.pack('f', self.cell[2*d+1]))

        writefile.write(self.header)
        header_items=len(self.header.split())

        for i in range(self.nb_atoms):
            writefile.write(struct.pack('i', i+1))
            writefile.write(struct.pack('f', self.x[i]))
            writefile.write(struct.pack('f', self.y[i]))
            writefile.write(struct.pack('i', self.ix[i]))
            writefile.write(struct.pack('i', self.iy[i]))
            writefile.write(struct.pack('f', self.rad[i]))
            if header_items > 8: 
                writefile.write(struct.pack('f', self.vx[i]))
                writefile.write(struct.pack('f', self.vy[i]))

        writefile.close()
        return 0


    def writeBinPairFile(self, readfile):
        wfilename = readfile+'-ts-'+str(self.tsteps)+'.bin' 
        sys.stderr.write("## writing "+wfilename+"\n")
        writefile = open(wfilename,'wb')
        writefile.write(struct.pack('i', self.tsteps))
        writefile.write(struct.pack('i', self.nb_entries))
        for d in range(3):
            writefile.write(struct.pack('f', self.cell[2*d]))
            writefile.write(struct.pack('f', self.cell[2*d+1]))
            
        writefile.write(self.header)
        for i in range(self.nb_entries):
            writefile.write(struct.pack('i', i+1))
            writefile.write(struct.pack('i', self.p1[i]))
            writefile.write(struct.pack('i', self.p2[i]))
            writefile.write(struct.pack('f', self.p3[i]))
            writefile.write(struct.pack('f', self.p4[i]))
            writefile.write(struct.pack('f', self.p5[i]))
            writefile.write(struct.pack('i', self.p6[i]))
            writefile.write(struct.pack('f', self.p7[i]))
            writefile.write(struct.pack('f', self.p8[i]))
            writefile.write(struct.pack('f', self.p9[i]))
            writefile.write(struct.pack('f', self.p10[i]))
            writefile.write(struct.pack('f', self.p11[i]))
            writefile.write(struct.pack('f', self.p12[i]))
            writefile.write(struct.pack('f', self.p13[i]))
            writefile.write(struct.pack('f', self.p14[i]))
            writefile.write(struct.pack('f', self.p15[i]))
            
        writefile.close()
        return 0


    def writeInit(self):
        wf = open("initconf.d", "w")
        print >> wf, "# initial configuration"
        print >> wf
        print >> wf, self.nb_atoms, "atoms"
        # print >> wf, self.nb_atoms, "ellipsoids"
        print >> wf
        print >> wf, "1 atom types"
        print >> wf
        print >> wf,str("%.6f"%self.cell[0]).rjust(16),str("%.6f"%self.cell[1]).rjust(16),"xlo xhi"
        print >> wf,str("%.6f"%self.cell[2]).rjust(16),str("%.6f"%self.cell[3]).rjust(16),"ylo yhi"
        print >> wf,str("%.6f"%self.cell[4]).rjust(16),str("%.6f"%self.cell[5]).rjust(16),"zlo zhi"
        print >> wf
        print >> wf, "Masses"
        print >> wf
        print >> wf, "1 1.0"
        print >> wf
        print >> wf, "Atoms"
        print >> wf
        for i in range(self.nb_atoms):
            print >> wf, str(i+1).rjust(6), "1".rjust(5), str("%2.6e"%(self.x[i])).rjust(15), str("%2.6e"%(self.y[i])).rjust(15), str("%2.6e"%0).rjust(15)
            # print >> wf, str(i+1).rjust(6), "1".rjust(5), "1".rjust(5), str("%1.6e"%1.909859).rjust(15), str("%2.6e"%(self.x[i])).rjust(15), str("%2.6e"%(self.y[i])).rjust(15), str("%2.6e"%0).rjust(15)
        print >> wf
        #print >> wf, "Ellipsoids"
        print >> wf, "Radius"
        print >> wf
        for i in range(self.nb_atoms):
            #dm = 2*self.rad[i]
            #print >> wf, str(i+1).rjust(6), str("%1.6e"%dm).rjust(15), str("%1.6e"%dm).rjust(15), str("%1.6e"%dm).rjust(15), 
            #print >> wf, str("%2.6e"%(self.q1[i])).rjust(15), str("%2.6e"%(self.q2[i])).rjust(15), 
            #print >> wf, str("%2.6e"%(self.q3[i])).rjust(15), str("%2.6e"%(self.q4[i])).rjust(15)
            print >> wf, i+1, "   ", self.rad[i]

        wf.close()
        return 0

    def deleteParticles(self):
        # locate the center of the box
        cx = 0.5*(self.cell[0]+self.cell[1])
        cy = 0.5*(self.cell[2]+self.cell[3])
        
        did = []
        dynamicnb = self.nb_atoms
        i=0
        while (i < dynamicnb):
            r2  = (self.x[i]-cx)**2
            r2 += (self.y[i]-cy)**2
            
            if (r2<=2):
                did.append(i)
                print i,
                self.rad.pop(i)
                self.x.pop(i)
                self.y.pop(i)
                self.vx.pop(i)
                self.vy.pop(i)
                self.q1.pop(i)
                self.q2.pop(i)
                self.q3.pop(i)
                self.q4.pop(i)
                print i,
                dynamicnb -= 1
            else:
                i +=1


        self.nb_atoms = len(self.x)
        print self.nb_atoms
        
        
##############################################################################




            
                



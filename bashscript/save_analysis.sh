#!/bin/sh 
echo $1
for i in 32 33 34 35 
do
    
    if [ -d '/media/niepin/T3Disk/7.np_fix_active/dr0.001/va0.09/phi0.'$i'/mu0.9_N10000/dumps/' ]; then
	
	cd 'phi0.'$i'/mu0.9_N10000/dumps/'
	cp /media/niepin/T3Disk/10.voro_code/* .
	./compile.x 
	./a.out dumpfile.0100000000.txt 
	python sort_bin.py local_density.dat 50 $1 $i
	cd ../../../
	echo $i
	
    fi
    
done

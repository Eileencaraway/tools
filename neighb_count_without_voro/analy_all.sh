#!/bin/bash
./compile.x
echo $1
for((i=1;i<10;i+=1))
do 
./a.out 'dumpfile.00000'$i'0000.txt' 
mv local_density.dat 'local_density-'$i'0000-'$1'.dat' 
done
for((i=1;i<10;i+=1))
do 
./a.out 'dumpfile.0000'$i'00000.txt' 
mv local_density.dat 'local_density-'$i'00000-'$1'.dat' 
done 
for((i=1;i<10;i+=1))
do 
./a.out 'dumpfile.000'$i'000000.txt' 
mv local_density.dat 'local_density-'$i'000000-'$1'.dat' 
done
for((i=1;i<10;i+=1))
do 
./a.out 'dumpfile.00'$i'0000000.txt' 
mv local_density.dat 'local_density-'$i'0000000-'$1'.dat' 
done 


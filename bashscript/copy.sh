#!/bin/bash 

for i in 32 33 34 35 36 37
do 

./a.out 10000 '0.'$i'' 3 
cp  in.active initconf.d 'phi0.'$i'/mu0.0_N10000/'
sed 's_mu\ equal\ 0.0_mu\ equal\ 0.9_'< in.active > test 
cp test in.active
cp  in.active initconf.d 'phi0.'$i'/mu0.9_N10000/'
sed 's_mu\ equal\ 0.9_mu\ equal\ 0.0_'< in.active > test 
cp test in.active


done 


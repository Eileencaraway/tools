#!/bin/sh
 
for i in 32 33 34 35 36 37 
do 
mkdir 'phi0.'$i''
cd 'phi0.'$i''
mkdir mu0.0_N10000
mkdir mu0.9_N10000
cd ..
done 

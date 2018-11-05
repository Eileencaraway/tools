#!/bin/bash
echo $1 $2 
qsub submitActive.sh
sed 's_mu0.0_mu0.9_' < submitActive.sh > test1
cp test1 submitActive.sh 
qsub submitActive.sh 
sed 's_mu0.9_mu0.0_' < submitActive.sh > test1 
cp test1 submitActive.sh 
sed 's_phi0.'$1'_phi0.'$2'_'< submitActive.sh > test 
cp test submitActive.sh 



#/bin/bash

#PBS -P personal-pnie001
#PBS -N va0.09phi0.32
#PBS -j oe
#PBS -V
#PBS -m e 
#PBS -l select=2:ncpus=24
#PBS -l walltime=24:00:00 

cd $PBS_O_WORKDIR 
NCPUS=`cat $PBS_NODEFILE | wc -l` 
echo $NCPUS 

module load intelmpi

cd $HOME/scratch/7.np_fix_active/
cd dr0.001/va0.09/phi0.32/mu0.9_N10000/
mpirun -np 48 ../../lmp_mpi -in in.active 

exit 

#!/bin/sh
#PBS -l nodes=1:ppn=1
#PBS -l walltime=99:00:00
#PBS -j oe
#PBS -o error_log_RH_RP_DH.txt


cd $PBS_O_WORKDIR

python3 ../ICOW_RH_RP_DH.py BorgMOEA 5000 200 500000 100000000 81c

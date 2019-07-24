#!/bin/sh
#PBS -l nodes=1:ppn=1
#PBS -l walltime=99:00:00
#PBS -j oe
#PBS -o error_log_00200.txt


cd $PBS_O_WORKDIR

python3 ../ICOW_RH_RP_WH_DB_DH.py  BorgMOEA 200 200 5000000 500000 states_200_500K_

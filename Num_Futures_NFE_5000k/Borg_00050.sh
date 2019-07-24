#!/bin/sh
#PBS -l nodes=1:ppn=1
#PBS -l walltime=99:00:00
#PBS -j oe
#PBS -o error_log_00050.txt


cd $PBS_O_WORKDIR

python3 ../ICOW_RH_RP_WH_DB_DH.py  BorgMOEA 50 200 5000000 5000000 states_50_5000K_

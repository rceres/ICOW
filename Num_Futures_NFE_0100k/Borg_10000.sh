#!/bin/sh
#PBS -l nodes=1:ppn=1
#PBS -l walltime=99:00:00
#PBS -j oe
#PBS -o error_log_10000.txt


cd $PBS_O_WORKDIR

python3 ../ICOW_RH_RP_WH_DB_DH.py  BorgMOEA 10000 200 5000000 100000 states_10000_100K_

#!/bin/sh
#PBS -l nodes=1:ppn=1
#PBS -l walltime=99:00:00
#PBS -j oe
#PBS -o error_log_WH.txt


cd $PBS_O_WORKDIR

python3 ../ICOW_WH.py BorgMOEA 5000 200 10000000 100000 81c

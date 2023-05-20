#!/bin/sh
#SBATCH --job-name=nsga-syn
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=sywang33@connect.hku.hk
#SBATCH --partition=amd
#SBATCH --qos=normal
#SBATCH --ntasks=10
#SBATCH --nodes=1
#SBATCH --time=3-10:00:00
#SBATCH --output=/home/sywang33/SPO/BATCHOUTPUT/%x_%j.out
#SBATCH --error=/home/sywang33/SPO/BATCHOUTPUT/%x_%j.err

date
cd /home/sywang33/SPO/CODE/nsga_baseline/
python main.py --mp 0.8 --cp 0.05 --iter 1000 --upbound 100 --cc 0

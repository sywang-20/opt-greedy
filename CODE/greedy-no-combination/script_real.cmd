#!/bin/sh
#SBATCH --job-name=new-syn-test
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=sywang33@connect.hku.hk
#SBATCH --partition=amd
#SBATCH --qos=normal
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=3-10:00:00
#SBATCH --output=/home/sywang33/opt-greedy/BATCHOUTPUT/%x_%j.out
#SBATCH --error=/home/sywang33/opt-greedy/BATCHOUTPUT/%x_%j.err

cd /home/sywang33/opt-greedy/CODE/greedy
python main-syn.py --size 1000 --new_plans 5 --num_of_individual 20


#!/bin/sh
#SBATCH --job-name=new-syn
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
sizes=(100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500 1600 1700 1800 1900 2000 2500 3000)
for size in "${sizes[@]}"
do
python main-syn.py --size $size --new_plans 5 --num_of_individual 20&
done

wait

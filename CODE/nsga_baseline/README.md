- /CODE/nsga_baseline/目录下的代码实现了NSGA-II 方法的baseline
- 在运行baseline之前确保已经使用/CODE/nsga_precomputation/中的代码对网络数据进行预处理，预处理生成的数据应当存放在对应的网络数据中的/prepared/目录下
- 可以修改script.cmd中的脚本命令，在命令行窗口输入**sbatch script.cmd**，运行baseline的simulation



```bash
#SBATCH --job-name=SSP-simu
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=3180103434@zju.edu.cn
#SBATCH --partition=amd
#SBATCH --qos=normal
#SBATCH --ntasks=1
#SBATCH --nodes=1
#SBATCH --time=3-10:00:00
#SBATCH --output=/lustre1/g/upad_yzhou/SSP_PACKUP/BATCHOUTPUT/%x_%j.out
#SBATCH --error=/lustre1/g/upad_yzhou/SSP_PACKUP/BATCHOUTPUT/%x_%j.err

# print the start time
date

# commmand 
cd /lustre1/g/upad_yzhou/SSP_PACKUP/CODE/nsga_baseline
# 修改main.py中的参数，运行main.py进行计算
python main.py --mp 0.8 --cp 0.05 --iter 5 --upbound 100 --cc 0

```

- sbatch script.cmd的运行结果会被输出到 /lustre1/g/upad_yzhou/SSP_PACKUP/BATCHOUTPUT/和/lustre1/g/upad_yzhou/SSP_PACKUP/BATCHOUTPUT/目录下
- 命令行参数介绍（结合nsga_baseline/main.py理解）
  - --mp 对应mutation parameter
  - --cp 对应crossover parameter
  - --iter 对应NSGA算法的迭代次数
  - --upbound对应sensor number的上界
  - --cc用于限制新生成的individual的coverage，新生成的individual coverage>=total coverage *cc
  - --netdir 对应网络数据文件目录
  - --outdir simulation结果的输出目录
- 使用默认的的outdir参数时，结果输出到/TESTOUTPUT/real_life_case_nsga/目录下，按照指定的mp和cp等参数生成目录名，目录中的第0个文件夹存放了在该参数组合下的第0次simulation的解


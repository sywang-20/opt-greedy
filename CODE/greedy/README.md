- /CODE/local_search/greedy-nondominated/目录下的代码实现了依据nondominated sorting 方法排序的greedy algorithm 方法baseline
- 可以修改script.cmd的书写方式和/nsga_baseline/中的脚本命令类似，只需修改对应的运行参数即可，在命令行窗口输入**sbatch script.cmd**，运行baseline的simulation



```bash
parser.add_argument("--iter", type=int, default=5, help="the iteration number")
parser.add_argument("--upbound", type=int, default=100, help="the sensor upbound")
parser.add_argument("--lowbound", type=int, default=1, help="the sensor lower bound")
parser.add_argument("--case", type=int, default=0, help="0-real life case, other-synthetic case")
parser.add_argument("--datadir", type=str, default="../../../DATA/real_life_case_network/data/")
parser.add_argument("--outdir", type=str, default="../../../TESTOUTPUT/local_search/nondominated/")
```

- 命令行参数介绍（结合CODE/local_search/greedy-nondominated/main.py理解）
  - --iter对应迭代次数
  - --upbound和--lowbound对应initialization时的sensor number的上界和下界
  - --case的值为0时表明现在运行的时real life case，case!=0时是synthetic case
  - --datadir 对应网络数据文件目录
  - --outdir simulation结果的输出目录
- 使用默认的的outdir参数时，结果输出到/TESTOUTPUT/local_search/greedy-nondominated目录下，目录中的第0个文件夹存放了在该参数组合下的第0次simulation的解



- 每一个iteration将前一步的solution考虑进去，一起sorting，如果有进步，update成变好的solution，如果没有进步，则保留原始的
- nondominated sorting的依据： objective function
- stopping criterion： 
- 1. solution中sensor number最大的超过upper bound或者coverage和search cost
- 2. coverage和search cost 的 increment MSE 小于预定threshold

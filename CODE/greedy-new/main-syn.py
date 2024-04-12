import matplotlib.pyplot as plt
import networkx as nx
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import math
# from nsga.evolution import Evolution
# from nsga.problem import Problem
from evolution import Evolution
from problem import Problem
# from nsga import precomputation
# from nsga import objective
#import precomputation
import objective
import math
import pickle
import argparse
import os
import constraint
import time

'''
对synthetic case进行计算
'''

if __name__=='__main__':
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")

    # 需要用的参数都直接修改default，只留一个size
    parser = argparse.ArgumentParser(usage="it's usage tip.", description="help info.")
    #parser.add_argument("--max_sensor", type=int, default=5, help="upper bound of the number of sensors")  # sensor number的upper bound
    parser.add_argument("--num_of_individual", type=int, default=10, help="the number of reserved plans in each step")
    # parser.add_argument("--datadir", type=str, default="../../../DATA/synthetic_network/data/")  # 对应网络数据的保存目录
    # parser.add_argument("--outdir", type=str,
    #                     default="../../../TESTOUTPUT/local_search/greedy_nondominated_parameter_latest/")  # 对应输出结果的保存目录
    parser.add_argument("--size", type=int, default=100, help="the size of the network")


    args = parser.parse_args()

    # 读取前面的各类参数
    #max_sensor = args.max_sensor
    # output_dir = args.outdir
    # parent_dir = args.datadir
    num_of_individuals = args.num_of_individual
    size= args.size
    max_sensor=int(size/10)

    case_dir="../../DATA/synthetic_network/"+str(size)+"/"
    # 数一下这个size下有多少个不同网络。若使用这个，则是遍历所有同一size的synthetic network
    # count = 0
    # for file in os.listdir(case_dir):  # file 表示的是文件名
    #     count += 1

    # 选取一个作为例子
    count = 0

    # 创建结果文件夹+读取synthetic network
    for i in range(count+1):
        sol_dir= '../../TESTOUTPUT/synthetic_case/greedy_original/'+str(size)+'/'+str(i)
        if os.path.exists(sol_dir):
            continue
        # if not os.path.exists(sol_dir):
        #     os.makedirs(sol_dir)
        #     print('create directory successfully')
        # else:
        #     continue

        with open(case_dir+str(i)+"/prepared-new/upstream_set.pkl", "rb") as tf:
            upstream_set = pickle.load(tf)
        tf.close()

        with open(case_dir+str(i)+"/prepared-new/upstream_arr.pkl", "rb") as tf:
            upstream_arr = pickle.load(tf)
        tf.close()

        fn = case_dir+str(i)+"/prepared-new/syn.pkl"
        relabeled_G = nx.read_gpickle(fn)
        node_num = len(relabeled_G.nodes())
        print(node_num)

        with open(case_dir+str(i)+"/prepared-new/conn_dict.pkl", "rb") as tf:
            conn_dict = pickle.load(tf)
        tf.close()


        sample=np.ones(len(upstream_arr))

        problem = Problem(objectives=[objective.coverage,objective.search_cost],
                          constraint=[constraint.sensor_num],
                          node_num=node_num, upstream_arr=upstream_arr,
                         upstream_set=upstream_set,graph=relabeled_G,conn_dict=conn_dict)

        fig_path = '../../TESTOUTPUT/synthetic_case/greedy_original/'+str(size)+'/'+str(i)+'/'+'max_sensor_' + str(max_sensor) + '_Lmax_' + str(num_of_individuals)+'/'

        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        suffix=0
        for file in os.listdir(fig_path):
            suffix+=1
        fig_path=fig_path+str(suffix)


        evo = Evolution(problem, max_sensor=max_sensor, num_of_individuals=num_of_individuals,
                        fig_path=fig_path, node_num=node_num)

        print("start")
        start = time.time()
        evo.evolve()
        end=time.time()

        with open(os.path.join(fig_path, "time.txt"), "w") as tf:
            tf.write(str(end - start))

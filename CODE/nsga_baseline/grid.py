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
import precomputation
import objective
import math
import pickle

if __name__=='__main__':

    with open("E:/sewage-sensor-placement/extract_topo_graph/data/prepared/upstream_set.pkl", "rb") as tf:
        upstream_set = pickle.load(tf)
    tf.close()

    with open("E:/sewage-sensor-placement/extract_topo_graph/data/prepared/upstream_arr.pkl", "rb") as tf:
        upstream_arr = pickle.load(tf)
    tf.close()

    fn = 'E:/sewage-sensor-placement/extract_topo_graph/data/prepared/pipe_TM_clean_relabel.pkl'
    relabeled_G = nx.read_gpickle(fn)
    node_num=len(relabeled_G.nodes())
    print(node_num)

    # with open("../prepared/upstream_set.pkl", "rb") as tf:
    #     upstream_set = pickle.load(tf)
    # tf.close()
    #
    # with open("../prepared/upstream_arr.pkl", "rb") as tf:
    #     upstream_arr = pickle.load(tf)
    # tf.close()
    #
    # fn = '../prepared/pipe_TM_clean_relabel.pkl'
    # relabeled_G = nx.read_gpickle(fn)
    # node_num=len(relabeled_G.nodes())
    # print(node_num)

    a_up=[]

    # a_val=[0.2,0.4,0.6,0.8]
    # a_val=[0.4,0.6,0.8]
    # a_val=[0.4]
    # b_val=[0.1,0.15,0.2,0.25,0.3]
    # b_val=[0.05,0.1,0.15,0.2,0.25,0.3]
    a_val=[0.8]
    b_val=[0.05]

    # a_val = [0.8]
    # b_val = [0.05]

    # for i in range(1):
    for a in a_val:
        for b in b_val:


            # t=2
            # sample = np.random.exponential(t, len(upstream_set))
            # with open('./priority.pkl','wb') as f:
            #     pickle.dump(sample,f)

            # print(max(sample))
            # print(min(sample))
            sample=np.ones(len(upstream_arr))

        # # problem = Problem(num_of_variables=1, objectives=[coverage, sensor_num, search_cost], edge_num=edge_num, expand=False)
            problem = Problem(objectives=[objective.sensor_num, objective.coverage_by_topology,
                                          objective.new_search_cost_by_topology], node_num=node_num,
                              upstream_arr=upstream_arr,upstream_set=upstream_set,sensor_upbound=100,graph=relabeled_G,priority=sample)
            # problem = Problem(objectives=[objective.sensor_num, objective.coverage,
            #                               objective.new_search_cost], node_num=node_num,
            #                   upstream_arr=upstream_arr,
            #                   upstream_set=upstream_set, sensor_upbound=40, graph=relabeled_G, priority=sample)

            gen_num = 1000
            fig_path = 'E:/sewage-sensor-placement/output/test_topo' + str(gen_num) + '/'
            evo = Evolution(problem, num_of_generations=gen_num, num_of_individuals=200, num_of_tour_particips=2,
                            tournament_prob=0.8,
                            crossover_param=a, mutation_param=b, fig_path=fig_path)

            solution = evo.evolve()
            goals = [i.objectives for i in solution]

            coverage_goal = [i[0] for i in goals]
            sensor_num_goal = [i[1] for i in goals]
            search_cost_goal = [i[2] for i in goals]


        print('front[0] len:', len(coverage_goal))

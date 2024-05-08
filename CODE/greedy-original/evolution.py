# from nsga.utils import NSGA2Utils
# from nsga.population import Population
from utils import NSGA2Utils
from population import Population
# import time
# from time import sleep
from tqdm import tqdm
# from progress.bar import IncrementalBar
from progressbar import *
import matplotlib.pyplot as plt
import numpy as np
import os
import json
import pickle


class Evolution:
    def __init__(self, problem, max_sensor=5, num_of_individuals=100,
                 fig_path='./output/',sol={}, node_num=10):
        print('init Evolution')
        self.utils = NSGA2Utils(problem, num_of_individuals)
        self.population = None
        self.initial_population = None
        self.max_sensor = max_sensor  # max_sensor: 最终方案需要多少个sensor
        #self.new_plans_num = new_plans_num   # 每个iteration生成多少新plan
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals   # 每个iteration保留多少个plan
        #self.batch_size = batch_size
        self.fig_path = fig_path
        self.initial_individual = None
        self.sol=sol
        self.node_num=node_num

    def evolve(self):
        fig_path = self.fig_path

        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        self.population = self.utils.create_initial_population()

        solutions_dict = {}

        i = 0
        print('sensor number upper bound: '+str(self.max_sensor))
        print('reserved number of plans at each iteration: '+str(self.num_of_individuals))

        while True:
            if i >= self.max_sensor:
                break
            else:
                neighbors = Population()
                for j in self.population:
                    j_neighbor = self.utils.problem.create_individual_one_more_sensor_all(j)
                    neighbors.extend(j_neighbor)

                neighbors=self.utils.duplication_elimination(neighbors)

                #------fast non-dominated sorting，进行Lmax个解的选择----------
                self.utils.fast_nondominated_sort(neighbors)
                new_population = Population()
                front_num = 0

                # 前一步选取出来的solution，加上目前该front的数，比想要的solution总数小，把这个front的解全部加进去
                while len(new_population) + len(neighbors.fronts[front_num]) <= self.num_of_individuals:
                    self.utils.calculate_crowding_distance(neighbors.fronts[front_num])
                    new_population.extend(neighbors.fronts[front_num])  # 把这个front全部加进去
                    front_num += 1  # 更新front
                    print(front_num)

                print('final front num', front_num)  # 第一个不满足while判断的front，可能只有部分可以加进去
                self.utils.calculate_crowding_distance(neighbors.fronts[front_num])  # 对这个front的crowding distance进行计算
                neighbors.fronts[front_num].sort(key=lambda individual: individual.crowding_distance,reverse=True)  # 计算了crowding distance后，对其进行排序
                new_population.extend(neighbors.fronts[front_num][0:self.num_of_individuals - len(new_population)])  # 把符合数量要求的solution加进去

                self.population = new_population

                solutions_dict[i] = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                                    self.population]

            i=i+1

        with open(self.fig_path + '/solution.pkl', 'wb') as f:
            pickle.dump(solutions_dict, f)



    # calculate the objective function for one specific placement
    def evolve_new_syn(self):
        # calculate the objective function for one specific placement
        solution_obj = {}
        temp = []
        solution_temp = self.utils.problem.generate_individual_with_positive_nodes(self.sol)
        # print([solution_temp.objectives[0],solution_temp.objectives[1],solution_temp.objectives[2]])
        temp.append([solution_temp.objectives[0], solution_temp.objectives[1], solution_temp.objectives[2]])
        print(temp)

        print(solution_obj)

    def evolve_new(self):
        # calculate the objective function for one specific placement
        solution_obj = {}
        to_cal = ['indegree', 'outdegree', 'upstream_size', 'closeness_centrality', 'betweenness_centrality',
                  'katz_centrality', 'random']
        # to_cal=['random']
        for x in to_cal:
            temp = []
            for ind in self.sol[x]:
                # print(ind)
                solution_temp = self.utils.problem.generate_individual_with_positive_nodes(ind)
                # print([solution_temp.objectives[0],solution_temp.objectives[1],solution_temp.objectives[2]])
                temp.append([solution_temp.objectives[0], solution_temp.objectives[1], solution_temp.objectives[2]])
                print(temp)

            solution_obj[x] = temp
            print(solution_obj)



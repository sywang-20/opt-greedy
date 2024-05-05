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
        #self.num_of_solutions = num_of_solutions
        #self.coverage_increment_max=coverage_increment_max   # coverage的stopping criterion
        #self.search_cost_increment_max=search_cost_increment_max  # search cost的stopping criterion

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
                for front in neighbors.fronts:
                    self.utils.calculate_crowding_distance(front)
                # 按照domination_count从小到大，crowding_distance从大到小进行排序 (domination_count表示一个solution被其他solution所支配的次数)
                neighbors.population.sort(key=lambda individual: (individual.domination_count, -individual.crowding_distance))
                self.population = neighbors.population[0:self.num_of_individuals]

                solutions_dict[i] = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                                    self.population]

            i=i+1

        with open(self.fig_path + '/solution.pkl', 'wb') as f:
            pickle.dump(solutions_dict, f)







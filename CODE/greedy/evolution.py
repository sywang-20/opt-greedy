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
    def __init__(self, problem, max_sensor=5, num_of_individuals=100,  #batch_size=10,
                 new_plans_num=20, #coverage_increment_max=500, search_cost_increment_max=0.01,
                 fig_path='./output/',sol={}, node_num=10):
        print('init Evolution')
        self.utils = NSGA2Utils(problem, num_of_individuals)
        self.population = None
        self.initial_population = None
        self.max_sensor = max_sensor  # max_sensor: 最终方案需要多少个sensor
        self.new_plans_num = new_plans_num   # 每个iteration生成多少新plan
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals   # 每个iteration保留多少个plan
        self.fig_path = fig_path
        self.initial_individual = None
        self.sol=sol
        self.node_num=node_num


    def evolve_no_filter(self):
        fig_path = self.fig_path
        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        # 创建一个空的population用于保存最终解
        population_final = Population()
        population_final_front0 = Population()

        # 初始化一个空的population
        self.population = self.utils.create_initial_population()
        population_dict = {}

        i = 0
        print('evolve-no-filter-before-sorting')
        print('sensor number upper bound: ' + str(self.max_sensor))
        print('reserved number of plans at each iteration: ' + str(self.num_of_individuals))
        print('number of new plans generated from one plan: ' + str(self.new_plans_num))

        while True:
            if len(population_final_front0) == self.num_of_individuals:  # stopping criteria： 最终解在front 0的数量超过规定数
                break
            else:
                neighbors = Population()
                for j in self.population:
                    j_neighbors = self.utils.problem.create_individual_one_more_sensor(j, self.new_plans_num)
                    neighbors.append(j)
                    neighbors.extend(j_neighbors)


                neighbors = self.utils.duplication_elimination(neighbors)  # 去重


                # ------fast nondominated sorting选取每个iteration保存下来的解-----------
                self.utils.fast_nondominated_sort(neighbors)

                # ------分析front 0中的解，满足constraint的保留到final solution，并去掉。--------
                to_remove = Population()
                to_remove.extend(ind for ind in neighbors if ind.constraint[0] == self.max_sensor)
                population_final.extend(ind for ind in neighbors.fronts[0] if ind.constraint[0] == self.max_sensor)

                for ind in to_remove:
                    neighbors.remove(ind)

                # 最终的解是population_final的front0的
                population_final=self.utils.duplication_elimination(population_final)
                self.utils.fast_nondominated_sort(population_final)

                if len(population_final.fronts[0]) >= self.num_of_individuals:
                    self.utils.calculate_crowding_distance(population_final.fronts[0])
                    population_final.fronts[0].sort(key=lambda individual: individual.crowding_distance, reverse=True)
                    population_final_front0.extend(population_final.fronts[0][0:self.num_of_individuals])

                if len(neighbors) < self.num_of_individuals:
                    self.population = neighbors
                    # generate新的individual，放的sensor的数量和最大的一样多
                    n_to_generate = self.num_of_individuals - len(neighbors)
                    total_sensor_num = [j.constraint[0] for j in neighbors]
                    n_positive_nodes = np.max(total_sensor_num)  # sensor数量的最大值
                    pop_supplement = self.utils.population_supplement(n_to_generate,n_positive_nodes)  # 生成sensor数量比目前最大sensor数量小的solution
                    self.population.extend(pop_supplement)
                else:
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

                # 记录每个iteration开始的solution，即上一个iteration的最终solution
                population_dict[i] = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                                      self.population]

            i = i + 1

        # 最终的满足constraint的解
        final_solutions_dict = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                                population_final_front0]

        # 中间过程每一个iteration保存下来的解
        with open(self.fig_path + '/population.pkl', 'wb') as f:
            pickle.dump(population_dict, f)
        # 最终解
        with open(self.fig_path + '/final_solution.pkl', 'wb') as f:
            pickle.dump(final_solutions_dict, f)

    def evolve_filter(self):
        fig_path = self.fig_path
        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        # 创建一个空的population用于保存最终解
        population_final = Population()
        population_final_front0=Population()

        # 初始化一个空的population
        self.population = self.utils.create_initial_population()

        population_dict = {}

        i=0
        print('evolve-add-filter-before-sorting')
        print('sensor number upper bound: '+str(self.max_sensor))
        print('reserved number of plans at each iteration: '+str(self.num_of_individuals))
        print('number of new plans generated from one plan: '+str(self.new_plans_num))

        while True:
            if len(population_final_front0) == self.num_of_individuals:  # stopping criteria： 最终解在front 0的数量超过规定数。提取出相应数量的解，所以应该是==
                break
            else:
                neighbors = Population()
                for j in self.population:
                    j_neighbor = self.utils.problem.create_individual_one_more_sensor(j,self.new_plans_num)
                    neighbors.append(j)
                    neighbors.extend(j_neighbor)

                neighbors=self.utils.duplication_elimination(neighbors) # 去重

                #------fast nondominated sorting选取每个iteration保存下来的解-----------
                # 先过constraint
                to_remove = Population()
                to_remove.extend(ind for ind in neighbors if ind.constraint[0] == self.max_sensor)
                # 对满足constraint的进行sorting，front 0的解放到final solution candidate set
                self.utils.fast_nondominated_sort(to_remove)
                population_final.extend(to_remove.fronts[0])

                for ind in to_remove:
                    neighbors.remove(ind)

                # 最终的解是population_final的front0的
                population_final = self.utils.duplication_elimination(population_final)
                self.utils.fast_nondominated_sort(population_final)

                # final solution candidate set中front 0 的解的数量超过想要的solution的数量，则取出这个解，放到population_final_front0中，然后停止loop
                if len(population_final.fronts[0]) >= self.num_of_individuals:
                    self.utils.calculate_crowding_distance(population_final.fronts[0])
                    population_final.fronts[0].sort(key=lambda individual: individual.crowding_distance,reverse=True)
                    population_final_front0.extend(population_final.fronts[0][0:self.num_of_individuals])


                #------check余下的解是否比Lmax多-------
                if len(neighbors) < self.num_of_individuals:
                    self.population = neighbors
                    # generate新的individual，放的sensor的数量和最大的一样多
                    n_to_generate = self.num_of_individuals - len(neighbors)
                    total_sensor_num = [j.constraint[0] for j in neighbors]
                    n_positive_nodes = np.max(total_sensor_num) # sensor数量的最大值
                    pop_supplement = self.utils.population_supplement(n_to_generate, n_positive_nodes) # 生成sensor数量比目前最大sensor数量小的solution
                    self.population.extend(pop_supplement)

                else:
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

                # 记录每个iteration开始的solution，即上一个iteration的最终solution
                population_dict[i] = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                                    self.population]

            i=i+1

        # 最终的满足constraint的解
        final_solutions_dict = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in population_final_front0]


        # 中间过程每一个iteration保存下来的解
        with open(self.fig_path + '/population.pkl', 'wb') as f:
            pickle.dump(population_dict, f)
        # 最终解
        with open(self.fig_path + '/final_solution.pkl', 'wb') as f:
            pickle.dump(final_solutions_dict, f)

    def evolve_no_combination(self):
        fig_path = self.fig_path

        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        self.population = self.utils.create_initial_population()

        solutions_dict = {}

        i = 0
        print('evolve-no-combination')
        print('sensor number upper bound: ' + str(self.max_sensor))
        print('reserved number of plans at each iteration: ' + str(self.num_of_individuals))

        while True:
            if i == self.max_sensor:
                break
            else:
                neighbors = Population()
                for j in self.population:
                    # 每步生成一定数量的solution，但是不和上一个iteration的解合并
                    j_neighbor = self.utils.problem.create_individual_one_more_sensor(j, self.new_plans_num)
                    neighbors.extend(j_neighbor)

                neighbors = self.utils.duplication_elimination(neighbors)

                # ------fast non-dominated sorting，进行Lmax个解的选择----------
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

            i = i + 1

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

    # 简化的代码，但是是错的
    # # 计算front_num和crowding distance
    # self.utils.fast_nondominated_sort(neighbors)
    # new_population = Population()
    # for front in neighbors.fronts:
    #     self.utils.calculate_crowding_distance(front)
    # # 按照domination_count从小到大，crowding_distance从大到小进行排序 (domination_count表示一个solution被其他solution所支配的次数)
    # neighbors.population.sort(key=lambda individual: (individual.domination_count, -individual.crowding_distance))
    #
    # new_population=Population()
    # new_population.extend(neighbors.population[0:self.num_of_individuals])
    # self.population = new_population
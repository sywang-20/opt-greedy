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
        # print(first_population)

        if not os.path.exists(fig_path):
            os.makedirs(fig_path)
        # step 1：initialize the first population, with no sensor placed in the network，utils中具体generate的方法已经修改
        self.population = self.utils.create_initial_population()
        # # 初始5个individual没有问题
        for j in self.population:
            test=list(j.chromosome)
            print(test)

        # # 先给increment均值设置一些比较大的值，保证第一次循环可以进行
        # sensor_number_max=0

        solutions_dict = {}
        #population_dict = {}

        # # 收敛图由目标函数刻画
        # # objective function 1
        # goal1_of_all = []
        # q1_goal1_of_all=[]
        # q2_goal1_of_all = []
        # q3_goal1_of_all = []
        # # objective function 2
        # goal2_of_all = []
        # q1_goal2_of_all = []
        # q2_goal2_of_all = []
        # q3_goal2_of_all = []
        # # objective function 3
        # goal3_of_all = []
        # q1_goal3_of_all = []
        # q2_goal3_of_all = []
        # q3_goal3_of_all = []



        i = 0

        print('sensor number upper bound: '+str(self.max_sensor))
        print('reserved number of plans at each iteration: '+str(self.num_of_individuals))
        # print('number of new plans generated from one plan: '+str(self.new_plans_num))

        # neighbor理解为增加一个sensor后的solution
        # for i in range(self.max_sensor-1):  # search step这个循环条件修改为coverage和search cost的increment限制
        # 生成neighbors这一个对象，用于保存生成的neighbor individual
        while True:
            if i >= self.max_sensor:
                break
            else:
                neighbors = Population()
                for j in self.population:
                    # 遍历全部未选中的manhole，生成新的plan
                    j_neighbor = self.utils.problem.create_individual_one_more_sensor_all(j)
                    #print('number_of_new_plans for one solution in one iteration:'+str(len(j_neighbor)))
                    neighbors.extend(j_neighbor)


                neighbors=self.utils.duplication_elimination(neighbors)
                # print('number of neighbors for all solutions in one iteration: '+str(len(neighbors)))
                # for ind in neighbors:
                #     print(ind.chromosome)


                #------fast non-dominated sorting，进行Lmax个解的选择----------
                self.utils.fast_nondominated_sort(neighbors)

                cnt = 0
                for front in neighbors.fronts:
                    self.utils.calculate_crowding_distance(front)
                    cnt += 1

                # 生成一个空的新population class用于保存non-dominated sorting后选取的结果，并初始化front数为0
                new_population = Population()
                front_num = 0

                # 前一步选取出来的solution，加上目前该front的数，比想要的solution总数小，把这个front的解全部加进去
                while len(new_population) + len(neighbors.fronts[front_num]) <= self.num_of_individuals:
                    print('loop')
                    self.utils.calculate_crowding_distance(neighbors.fronts[front_num])
                    new_population.extend(neighbors.fronts[front_num])  # 把这个front全部加进去
                    front_num += 1  # 更新front
                    print(front_num)

                print('final front num', front_num)  # 第一个不满足while判断的front，可能只有部分可以加进去
                self.utils.calculate_crowding_distance(neighbors.fronts[front_num])  # 对这个front的crowding distance进行计算
                neighbors.fronts[front_num].sort(key=lambda individual: individual.crowding_distance,
                                             reverse=True)  # 计算了crowding distance后，对其进行排序
                new_population.extend(
                    neighbors.fronts[front_num][0:self.num_of_individuals - len(new_population)])  # 把符合数量要求的solution加进去

                self.population = new_population  # 得到一个新的population
                #--------每个iteration的Lmax个解选择完毕

                # self.utils.fast_nondominated_sort(self.population)  # 对新的population进行non-dominated sorting
                # for front in self.population.fronts:
                #     self.utils.calculate_crowding_distance(front)

                #print('sensor number in this step:' + str(i+1))
                #print('population len:' + str(len(self.population)))

                # 取出greedy-nondominated sorting得到的解中front 0的目标函数值以及sensor-placed manhole
                # solutions_dict[i] = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                #                     self.population.fronts[0]]
                # 取出所有solution的目标函数值以及sensor-placed manhole--> 这个得到的是greedy-nondominated algorithm的全部解
                solutions_dict[i] = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                                    self.population]


                # check每一步的sensor数量
                # total_val1=[j.constraint[0] for j in self.population]
                # sensor_number_max=np.max(total_val1)
                #
                #
                # total_val2=[-j.objectives[0]for j in self.population]  #coverage
                # total_val3=[j.objectives[1]for j in self.population]   #search cost
                #
                #
                # goal1_of_all.append(np.mean(total_val1))
                # q1_goal1_of_all.append(np.percentile(total_val1, 25))
                # q2_goal1_of_all.append(np.percentile(total_val1, 50))
                # q3_goal1_of_all.append(np.percentile(total_val1, 75))
                # goal2_of_all.append(np.mean(total_val2))
                # q1_goal2_of_all.append(np.percentile(total_val2, 25))
                # q2_goal2_of_all.append(np.percentile(total_val2, 50))
                # q3_goal2_of_all.append(np.percentile(total_val2, 75))
                # goal3_of_all.append(np.mean(total_val3))
                # q1_goal3_of_all.append(np.percentile(total_val3, 25))
                # q2_goal3_of_all.append(np.percentile(total_val3, 50))
                # q3_goal3_of_all.append(np.percentile(total_val3, 75))



            i=i+1

        # #print('search step(sensor_number)'+str(self.max_sensor))
        # plt.figure(figsize=(50, 20))
        # ax = plt.subplot(1, 3, 1)
        # ax.set_title('Avg Sensor Number in Whole Population', fontsize=20)
        # ax.plot(range(i-1),goal1_of_all)
        # ax.fill_between(range(i-1),q3_goal1_of_all,q1_goal1_of_all,alpha=0.2)
        # ax.fill_between(range(i-1),q3_goal1_of_all,q2_goal1_of_all,alpha=0.2,color='y')
        #
        # ax = plt.subplot(1, 3, 2)
        # ax.set_title('Avg Coverage in Whole Population', fontsize=20)
        # ax.plot(range(i-1),goal2_of_all)
        # ax.fill_between(range(i-1),q3_goal2_of_all,q1_goal2_of_all,alpha=0.2)
        # ax.fill_between(range(i-1),q3_goal2_of_all,q2_goal2_of_all,alpha=0.2,color='y')
        #
        # ax = plt.subplot(1, 3, 3)
        # ax.set_title('Avg Search Cost in Whole Population', fontsize=20)
        # ax.plot(range(i-1),goal3_of_all)
        # ax.fill_between(range(i-1),q3_goal3_of_all,q1_goal3_of_all,alpha=0.2)
        # ax.fill_between(range(i-1),q3_goal3_of_all,q2_goal3_of_all,alpha=0.2,color='y')
        # plt.savefig(self.fig_path + '/' + 'objective_function_plot.png')



        # with open(self.fig_path + '/solution.pkl', 'wb') as f:
        #     # pickle.dump(obj,file): 把对象obj保存到文件file中
        #     pickle.dump(solutions_dict, f)
        with open(self.fig_path + '/solution.pkl', 'wb') as f:
            pickle.dump(solutions_dict, f)



        # 最后一代
        # 最后一个循环，前面的终止条件是search_step-1，这个相当于把search_step那一步补上
        # 前面循环是根据batch_size选择每个循环neighbor的个数，最后一个循环是按照number of solutions来选择
        # neighbors = Population()
        # for j in self.population:
        #     j_neighbor = self.utils.problem.create_individual_one_more_sensor(j,self.new_plans_num)
        #     neighbors.extend(j_neighbor)
        #
        # self.utils.fast_nondominated_sort(neighbors)
        #
        # cnt = 0
        # for front in neighbors.fronts:
        #     self.utils.calculate_crowding_distance(front)
        #     print(cnt, 'front  len ', len(front))
        #     cnt += 1
        # #
        # new_population = Population()
        # front_num = 0
        #
        # while len(new_population) + len(neighbors.fronts[front_num]) <= self.num_of_solutions:
        #     print('loop')
        #     self.utils.calculate_crowding_distance(neighbors.fronts[front_num])
        #     new_population.extend(neighbors.fronts[front_num])
        #     front_num += 1
        #     print(front_num)
        # #
        # print('final front num', front_num)
        # self.utils.calculate_crowding_distance(neighbors.fronts[front_num])
        # neighbors.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
        # new_population.extend(neighbors.fronts[front_num][0:self.num_of_solutions - len(new_population)])
        # self.population = new_population
        #
        # self.utils.fast_nondominated_sort(self.population)
        # for front in self.population.fronts:
        #     self.utils.calculate_crowding_distance(front)
        #
        # solutions_dict[self.max_sensor - 1] = [[i.objectives[0], i.objectives[1], i.objectives[2], i.positive_nodes]
        #                                          for i in
        #                                          self.population.fronts[0]]
        #
        # population_dict[self.max_sensor - 1] = [[i.objectives[0], i.objectives[1], i.objectives[2], i.positive_nodes]
        #                                           for i in
        #                                           self.population]
        #




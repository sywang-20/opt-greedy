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



    def __init__(self, problem, search_steps=5, num_of_individuals=100,  #batch_size=10,
                 new_plans_num=25, #coverage_increment_max=500, search_cost_increment_max=0.01,
                 fig_path='./output/',sol={}, node_num=10):
        print('init Evolution')
        self.utils = NSGA2Utils(problem, num_of_individuals)
        self.population = None
        self.initial_population = None
        self.search_steps = search_steps  # search_steps: 最终方案需要多少个sensor
        self.new_plans_num = new_plans_num   # 每个iteration生成多少新plan
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

        population_final = Population()
        self.population = self.utils.create_initial_population()

        solutions_dict = {}
        population_dict = {}
        final_solutions_dict = {}

        # 收敛图由目标函数刻画
        # objective function 1
        goal1_of_all = []
        q1_goal1_of_all=[]
        q2_goal1_of_all = []
        q3_goal1_of_all = []
        # objective function 2
        goal2_of_all = []
        q1_goal2_of_all = []
        q2_goal2_of_all = []
        q3_goal2_of_all = []
        # objective function 3
        goal3_of_all = []
        q1_goal3_of_all = []
        q2_goal3_of_all = []
        q3_goal3_of_all = []


        i = 1

        print('sensor number upper bound: '+str(self.search_steps))
        print('reserved number of plans at each iteration: '+str(self.num_of_individuals))
        print('number of new plans generated from one plan: '+str(self.new_plans_num))

        while True:
            if len(population_final) >= self.num_of_individuals:
                break
            else:
                neighbors = Population()
                for j in self.population:
                    j_neighbor = self.utils.problem.create_individual_one_more_sensor(j,self.new_plans_num)
                    neighbors.append(j)
                    neighbors.extend(j_neighbor)

                print('number of neighbors: '+str(len(neighbors)))
                neighbors=self.utils.duplication_elimination(neighbors) # 去重
                print('number of neighbors-no-duplication: '+str(len(neighbors)))
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
                
                print('new population len-for final solution:' + str(len(new_population)))
                print('self.population len-before adding to final solution:' + str(len(self.population)))

                # 对于new population中的解，选择符合要求的加入final solution
                to_remove = Population()
                for ind in new_population:
                    if ind.constraint[0]==self.search_steps and len(population_final)<self.num_of_individuals:  # sensor number达到上限的solution
                        print(ind.constraint[0],ind.objectives[0],ind.objectives[1],ind.positive_nodes)
                        population_final.append(ind)
                        to_remove.append(ind)
                        print('final population len:' + str(len(population_final)))

                for ind in to_remove:
                    self.population.remove(ind)

                print('self.population len-after removing final solution:' + str(len(self.population)))
                #self.population = new_population  # 得到一个新的population

                # 去掉放入final solution的解，剩下的解选择num_of_individuals个加入下一步的population
                self.utils.fast_nondominated_sort(self.population)
                cnt = 0
                for front in self.population.fronts:
                    self.utils.calculate_crowding_distance(front)
                    cnt += 1

                new_population2 = Population()
                front_num = 0

                while len(new_population2) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                    print('loop')
                    self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                    new_population2.extend(self.population.fronts[front_num])  # 把这个front全部加进去
                    front_num += 1  # 更新front
                    print(front_num)

                print('final front num', front_num)  # 第一个不满足while判断的front，可能只有部分可以加进去
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])  # 对这个front的crowding distance进行计算
                self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance,
                                             reverse=True)  # 计算了crowding distance后，对其进行排序
                new_population2.extend(
                    self.population.fronts[front_num][0:self.num_of_individuals - len(new_population2)])
                

                # 得到一个新的population
                self.population = new_population2  
                
                print('self.population len-adding to next step:' + str(len(self.population)))

                # sorting后保存解
                self.utils.fast_nondominated_sort(self.population)  # 对新的population进行non-dominated sorting
                for front in self.population.fronts:
                    self.utils.calculate_crowding_distance(front)
                self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance,
                                                       reverse=True)

                print('search step:' + str(i))
                print('population len:' + str(len(self.population)))

                # 取出greedy-nondominated sorting得到的解中front 0的目标函数值以及sensor-placed manhole
                solutions_dict[i] = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                                    self.population.fronts[0]]
                # 取出所有solution的目标函数值以及sensor-placed manhole--> 这个得到的是greedy-nondominated algorithm的全部解
                population_dict[i] = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in
                                    self.population]

                sen_num=[i.constraint[0] for i in self.population]
                max_sensor_num=max(sen_num)
                print('max sensor number: '+str(max_sensor_num))
                print('sensor number:'+str(sen_num))

                total_val1=[j.constraint[0]for j in self.population]   # sensor number
                total_val2=[-j.objectives[0]for j in self.population]  # coverage
                total_val3=[j.objectives[1]for j in self.population]   # search cost


                goal1_of_all.append(np.mean(total_val1))
                q1_goal1_of_all.append(np.percentile(total_val1, 25))
                q2_goal1_of_all.append(np.percentile(total_val1, 50))
                q3_goal1_of_all.append(np.percentile(total_val1, 75))
                goal2_of_all.append(np.mean(total_val2))
                q1_goal2_of_all.append(np.percentile(total_val2, 25))
                q2_goal2_of_all.append(np.percentile(total_val2, 50))
                q3_goal2_of_all.append(np.percentile(total_val2, 75))
                goal3_of_all.append(np.mean(total_val3))
                q1_goal3_of_all.append(np.percentile(total_val3, 25))
                q2_goal3_of_all.append(np.percentile(total_val3, 50))
                q3_goal3_of_all.append(np.percentile(total_val3, 75))

                # to_remove = Population()
                # for ind in self.population:
                #     if ind.constraint[0]==self.search_steps and len(population_final)<self.num_of_individuals:  # sensor number达到上限的solution
                #         print(ind.constraint[0],ind.objectives[0],ind.objectives[1],ind.positive_nodes)
                #         population_final.append(ind)
                #         to_remove.append(ind)
                #         print('final population len:' + str(len(population_final)))

                # for ind in to_remove:
                #     self.population.remove(ind)

                # final=len(population_final)
                # print('final population len:' + str(final))

                # final_solutions_dict = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in population_final]

            i=i+1
        
        final_solutions_dict = [[i.constraint[0], i.objectives[0], i.objectives[1], i.positive_nodes] for i in population_final]

        # 画图
        plt.figure(figsize=(50, 20))
        ax = plt.subplot(1, 3, 1)
        ax.set_title('Avg Sensor Number in Whole Population', fontsize=20)
        ax.plot(range(i-1),goal1_of_all)
        ax.fill_between(range(i-1),q3_goal1_of_all,q1_goal1_of_all,alpha=0.2)
        ax.fill_between(range(i-1),q3_goal1_of_all,q2_goal1_of_all,alpha=0.2,color='y')

        ax = plt.subplot(1, 3, 2)
        ax.set_title('Avg Coverage in Whole Population', fontsize=20)
        ax.plot(range(i-1),goal2_of_all)
        ax.fill_between(range(i-1),q3_goal2_of_all,q1_goal2_of_all,alpha=0.2)
        ax.fill_between(range(i-1),q3_goal2_of_all,q2_goal2_of_all,alpha=0.2,color='y')

        ax = plt.subplot(1, 3, 3)
        ax.set_title('Avg Search Cost in Whole Population', fontsize=20)
        ax.plot(range(i-1),goal3_of_all)
        ax.fill_between(range(i-1),q3_goal3_of_all,q1_goal3_of_all,alpha=0.2)
        ax.fill_between(range(i-1),q3_goal3_of_all,q2_goal3_of_all,alpha=0.2,color='y')
        plt.savefig(self.fig_path + '/' + 'objective_function_plot.png')



        with open(self.fig_path + '/solution.pkl', 'wb') as f:
            pickle.dump(solutions_dict, f)
        with open(self.fig_path + '/population.pkl', 'wb') as f:
            pickle.dump(population_dict, f)
        with open(self.fig_path + '/final_solution.pkl', 'wb') as f:
            pickle.dump(final_solutions_dict, f)





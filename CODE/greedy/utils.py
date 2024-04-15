# from nsga.population import Population
from population import Population
import random
import time
import numpy as np
# from nsga import topology



class NSGA2Utils:
    """
        Implements util functions in the NSGA-II process.
        Attributes:
            problem = Current problem implementation.
            num_of_individuals: An Integer determining the population size in this NSGA-II simulation.
    """
    def __init__(self, problem, num_of_individuals):
        self.problem = problem
        self.num_of_individuals = num_of_individuals

        # self.node_num=problem.node_num


    def _choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        return False


    # @profile
    def create_initial_population(self):
    # 生成一个个solution
        population = Population()
    # num_of_individuals: solution的个数
        for i in range(self.num_of_individuals):
            # print(i,'th individual')
            # problem中generate_individual是生成单个individual的，修改这个让他只产生布置了一个sensor的解
            individual = self.problem.generate_individual_no_sensor()
            # 计算这些solution对应的objective function的值，这里不可以省掉，因为前后合并全是0的会被保存，需要有objective function！！！
            self.problem.calculate_objectives(individual)
            self.problem.calculate_constraint(individual)
            population.append(individual)
        return population

    def population_supplement(self,num_individual,n):
        # num_individual: 需要新生成的solution数量
        # n：每个solution里sensor的数量
        population=Population()
        for i in range(num_individual):
            individual=self.problem.generate_individual_supplement(n)
            self.problem.calculate_objectives(individual)
            self.problem.calculate_constraint(individual)
            population.append(individual)
        return population


    def fast_nondominated_sort(self, population):
        # 根据objective function进行sorting
        start = time.time()
        population.fronts = [[]]
        for individual in population:
            individual.domination_count=0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1

            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            # print('loop')
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            population.fronts.append(temp)
        end = time.time()
        print('\n' + 'Fast Nondominated Sorting Time: %fs' % (end - start))





    def calculate_crowding_distance(self, front):

        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                # print(front[0].objectives)
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10 ^ 9
                front[solutions_num - 1].crowding_distance = 10 ^ 9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0:
                    scale = 1
                for i in range(1, solutions_num - 1):
                    front[i].crowding_distance += (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / scale


    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or ((
                                                                 individual.rank == other_individual.rank) and individual.crowding_distance > other_individual.crowding_distance):
            return 1
        else:
            return -1

    # @profile
    # 新的！！！！增加一个sensor之后，把重复的sensor placement plan删掉
    def duplication_elimination(self,population):
        individual_no_duplication=Population()   # 而不是空的list
        for individual in population:
            if individual not in individual_no_duplication:
                individual_no_duplication.append(individual)
        return individual_no_duplication

    def duplication_elimination_v2(self,population):
        # 速度优化
        individual_no_duplication=Population()
        temp=list(set(tuple(i) for i in population))
        individual_no_duplication.extend(temp)
        return individual_no_duplication

    def duplication_constraint(self,population):
        individual_constraint=Population()
        for individual in population:
            if individual.constraint<=self.num_of_individuals:
                individual_constraint.append(individual)
        return individual_constraint
# from nsga.individual import Individual
from individual import Individual
import objective
# from nsga import topology
import topology
import random
import numpy as np
import time
import copy
from population import Population
def matrix_and(a, b):
    n = a.shape[0]
    c = np.zeros((n, n), dtype=int)
    for i in range(n):
        c[i] = a[i] & b[i]

    return c
class Problem:
    """
    Describes important constraints in the simulation implementation.
    Attributes:
        num_of_objectives = Number of objective functions.
        objectives = Objective functions.
        node_num = Number of nodes/manholes in the original graph.
        upstream_arr = The number of upstream nodes for each manhole.
        upstream_set = The list of the sets of upstream nodes for every manhole.
        sensor_upbound = The maximum number of positive manholes.
        graph = The original sewage sensor network.
        priority = An array determining the priority factor of each manhole.
        conn_dict = Connectivity of the original sewage sensor network.
        coverage_constrain = A Float constraining the minimum coverage by coverage_constrain*total coverage.
    """
    def __init__(self, objectives,node_num,upstream_arr,upstream_set,conn_dict={},graph=None,sol={}):
        """
        Problem object initialization
        """
        self.num_of_objective=len(objectives)
        self.objectives=objectives
        #self.objectives_increment=objectives_increment
        self.node_num=node_num
        self.upstream_arr=upstream_arr
        self.upstream_set=upstream_set
        #self.sensor_upbound=sensor_upbound
        #self.sensor_lowbound=sensor_lowbound
        self.graph=graph
        # self.priority=priority
        self.conn_dict=conn_dict
        self.sol=sol
        # self.conn_matrix=conn_matrix


    # @profile

    def generate_individual_with_positive_nodes(self,positive_nodes):
        # 多出来的
        individual=Individual(self.node_num)
        individual.positive_nodes=positive_nodes
        for i in positive_nodes:
            individual.chromosome[i]=1
        self.calculate_objectives(individual)

        return individual

    # new!!!!!
    def generate_individual_one_sensor(self):
        """
        生成只有一个sensor的individual
        """
        individual=Individual(self.node_num)  #一个和网络node个数一样的solution
        positive_num=0 # 原本是sensor numer上下界中取一个随机数n，设置n个sensor，现在修改为0个，即初始情况-->从0开始，这样循环里就是从1开始
        positive_nodes=random.sample(list(range(self.node_num)),positive_num)  #随机在网络中设置positive node，即布置sensor
        individual.positive_nodes=positive_nodes

        for i in positive_nodes:
            individual.chromosome[i]=1
        return individual


    def generate_individual(self):
        """
        Generate individual.

        Return:
            newly generated individual
        """
        individual=Individual(self.node_num)
        positive_num=random.randint(self.sensor_lowbound,self.sensor_upbound)
        positive_nodes=random.sample(list(range(self.node_num)),positive_num)
        individual.positive_nodes=positive_nodes

        for i in positive_nodes:
            individual.chromosome[i]=1
        return individual

    def generate_individual_with(self,individual1):
        """
        Copy an new individual.

        Args:
            individual1

        Return:
            individual
        """

        individual=Individual(self.node_num)
        individual.chromosome=individual1.chromosome
        # individual.Gsub=individual1.Gsub
        individual.positive_nodes=individual1.positive_nodes
        return individual


    # @profile
    def calculate_objectives(self, individual):
        """
        Calculate the objective values of a certain individual

        Args:
            individual

        """
        # using the Gsub
        # individual.positive_nodes=[3285,1137,3424]
        # individual.chromosome=np.zeros(len(self.upstream_arr))
        # for i in individual.positive_nodes:
        #     individual.chromosome[i]=1


        # individual.Gsub=topology.extract_connectivity_subgraph(self.graph,individual.chromosome)
        individual.Gsub=topology.extract_connectivity_fastdict(self.graph, individual.chromosome,self.conn_dict)
        # print('dict len:',len(self.conn_dict))

        downstream_node = [i[0] for i in individual.Gsub.out_degree() if i[1] == 0]  # Gsub中每个subgraph最下游的node
        coverage_set = set()
        for i in downstream_node:
            coverage_set = coverage_set | self.upstream_set[i]   # 按位或运算符，有一个就可以加到coverage_set中


        individual.coverage_set=coverage_set  # 得到每个solution的coverage set
        individual.objectives=[f(self,individual) for f in self.objectives]
        individual.positive_nodes = np.array(np.where(individual.chromosome == 1))[0].tolist()


    def create_individual_neighbor(self,individual):
        # 多出来的
        # print('create neighbor')
        individual.positive_nodes = np.array(np.where(individual.chromosome == 1))[0].tolist()  #取出chromosome中gene为1的index
        # individual_neighbor=Population()
        individual_neighbor=[]
        for i in individual.positive_nodes:
            i_neighbor=self.graph.to_undirected().neighbors(i)
            for neighbor_node in i_neighbor:
                temp_positive_nodes=copy.deepcopy(individual.positive_nodes)
                temp_positive_nodes.remove(i)
                temp_positive_nodes.append(neighbor_node)
                new_neighbor=self.generate_individual_with_positive_nodes(temp_positive_nodes)
                individual_neighbor.append(new_neighbor)
        return individual_neighbor

    # 创建子类，one more sensor继承前面individual的特征，再加上increment这一个东西

    # new!!!!每次多一个sensor，在这里把新individual的目标函数增量一起计算好

    def create_individual_one_more_sensor(self,individual,n):
        individual_updated=[]

        i=0
        while i<n:
            i_plan_num=0
            while True:
                if i_plan_num==1:
                    break
                else:
                    pos=np.random.randint(0,self.node_num)
                    if pos not in individual.positive_nodes:
                        i_plan_num=1
                        temp = individual.positive_nodes.copy()
                        temp.append(pos)
                        new_neighbor=self.generate_individual_with_positive_nodes(temp)  #这里有计算objective function
                        individual_updated.append(new_neighbor)
            i=i+1
        return individual_updated








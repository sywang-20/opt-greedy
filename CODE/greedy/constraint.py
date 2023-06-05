import math
import math
# from nsga import topology
# import topology
import networkx as nx
import numpy as np
def subtract_common(pre, temp):
    return pre-temp


#------------------------------sensor number计算-------------------------
def sensor_num(problem,individual):
    s = np.sum(individual.chromosome)
    # print('sensor num',s)
    return s
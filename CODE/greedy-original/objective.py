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


#-------------------------------search cost计算-------------------------
def search_cost(problem, individual):
    if np.sum(individual.chromosome) == 0:
        search_cost = 0
    else:
        # 首先转为undirected计算不连通的子集
        undirected_Gsub = individual.Gsub.to_undirected()
        nodeSet = [set(undirected_Gsub.subgraph(c).nodes()) for c in nx.connected_components(undirected_Gsub)]

        coverage_set = individual.coverage_set
        coverage = len(coverage_set)
        temp_Gsub = individual.Gsub
        search_cost = 0

        # 首先计算additional upstream
        additional_upstream = {}
        while coverage_set:
            upstream_nodes = [i[0] for i in temp_Gsub.in_degree() if i[1] == 0]
            for i in upstream_nodes:
                temp_set = coverage_set.intersection(problem.upstream_set[i])
                length = len(temp_set)

                additional_upstream[i] = len(temp_set)
                coverage_set.difference_update(problem.upstream_set[i])
                temp_Gsub.remove_node(i)

        for component in nodeSet:
            temp_coverage_set = set()
            for node in component:
                temp_coverage_set.update(problem.upstream_set[node])

            for node in component:
                if node in additional_upstream and additional_upstream[node] > 0:
                    search_cost += math.log(additional_upstream[node], 2) * additional_upstream[node] / coverage

    return search_cost


#-------------------------------coverage 计算-------------------------
def coverage(problem,individual):
    if np.sum(individual.chromosome) == 0:
        coverage = 0
    else:
        coverage = len(individual.coverage_set)
    return -coverage


def coverage_by_topology(problem,individual):
    downstream_node = [i[0] for i in individual.Gsub.out_degree() if i[1] == 0]
    coverage_set = set()
    for i in downstream_node:
        coverage_set = coverage_set | problem.upstream_set[i]
    coverage = len(individual.coverage_set)
    return -coverage


def coverage_with_priority(problem,individual):
    coverage=0
    # print(maindividual.priority)
    for i in individual.coverage_set:
        coverage+=problem.priority[i]
    return -coverage







# def new_search_cost(problem,individual):
#     if np.sum(individual.chromosome)==0:
#         search_cost=0
#     else:
#         positive_nodes = [i for i, x in enumerate(individual.chromosome) if x == 1]
#         positive_upstream = [problem.upstream_set[i] for i in positive_nodes]
#         positive_upsize = [problem.upstream_arr[i] for i in positive_nodes]
#         additional_upstream = {}
#         while positive_nodes:
#             index = positive_upsize.index(min(positive_upsize))
#             val = positive_upsize[index]
#             manhole_id = positive_nodes[index]
#
#             additional_upstream[manhole_id] = val
#             positive_nodes.remove(manhole_id)
#
#             new_pos_num = len(positive_nodes)
#             temp_set = [positive_upstream[index]] * new_pos_num
#
#             positive_upsize.remove(positive_upsize[index])
#             positive_upstream.remove(positive_upstream[index])
#
#             positive_upstream = list(map(subtract_common, positive_upstream, temp_set))
#             positive_upsize = [len(i) for i in positive_upstream]
#
#         # 然后计算bunch dict
#         bunch_dict = {}
#         bunch_coverage = {}
#         cnt = 0
#         # upstream_nodes = []
#         # print(additional_upstream)
#
#         upstream_nodes = [i for i, x in enumerate(individual.chromosome) if x == 1]
#         # print('up', upstream_nodes)
#         while len(upstream_nodes):
#             # print(len(upstream_nodes))
#             i = upstream_nodes[0]
#             upstream_nodes.remove(i)
#             ancestor = problem.upstream_set[i]
#             bunch_dict[cnt] = []
#             bunch_dict[cnt].append(i)
#             #     bunch_coverage[cnt]=set()
#             bunch_coverage[cnt] = problem.upstream_set[i]
#             temp_ancestor = ancestor
#             # while len(upstream_nodes):
#             for j in upstream_nodes:
#                 temp_ancestor = temp_ancestor.intersection(problem.upstream_set[j])
#                 if len(temp_ancestor) != 0:
#                     upstream_nodes.remove(j)
#                     bunch_dict[cnt].append(j)
#                     bunch_coverage[cnt] = bunch_coverage[cnt] | problem.upstream_set[j]
#             cnt += 1
#
#         search_cost = 0
#         for i in range(cnt):
#             bunch_size = len(bunch_coverage[i])
#
#             for j in bunch_dict[i]:
#                 search_cost += math.log(additional_upstream[j], 2) * additional_upstream[j] / bunch_size
#
#         search_cost=search_cost/np.sum(individual.chromosome)
#         print(search_cost)
#     return search_cost

# def search_cost_final(problem,individual):
#     positive_nodes=[i for i, x in enumerate(individual.chromosome) if x == 1]
#     positive_upstream=[problem.upstream_set[i] for i in positive_nodes]
#     positive_upsize=[problem.upstream_arr[i] for i in positive_nodes]
#
#     upstream_size={}
#
#     search_cost=0
#     while positive_nodes:
#         index = positive_upsize.index(min(positive_upsize))
#         val = positive_upsize[index]
#
#         # print(val)
#         search_cost += math.log(val, 2)*val/len(individual.chromosome)
#         positive_nodes.remove(positive_nodes[index])
#         new_pos_num = len(positive_nodes)
#         temp_set = [positive_upstream[index]] * new_pos_num
#         positive_upsize.remove(positive_upsize[index])
#         positive_upstream.remove(positive_upstream[index])
#
#         positive_upsize = [len(i) for i in positive_upstream]
#         positive_upstream = list(map(subtract_common, positive_upstream, temp_set))
#
#     if np.sum(individual.chromosome)==0:
#         search_cost=0
#     else:
#         search_cost = search_cost / np.sum(individual.chromosome)
#     return search_cost




# @profile
# Algo 1
# def search_cost_by_topology(problem,individual):
#     search_cost = 0
#     coverage_set=individual.coverage_set
#     while coverage_set:
#         upstream_nodes = [i[0] for i in individual.Gsub.in_degree() if i[1] == 0]
#         for i in upstream_nodes:
#             individual.Gsub.remove_node(i)
#             temp_set = coverage_set.intersection(problem.upstream_set[i])
#             length=len(temp_set)
#             if length>1:
#                 search_cost += math.log(len(temp_set),2)
#             coverage_set = coverage_set.difference(problem.upstream_set[i])
#
#     search_cost=search_cost/np.sum(individual.chromosome)
#     return search_cost

#

# def new_search_cost_by_topology(individual):
#     search_cost = 0
#     coverage_set=individual.coverage_set
#     temp_Gsub=individual.Gsub.copy()
#     additional_upstream = {}
#     additional_upset = {}
#     temp_positive_manholes=[i for i,x in enumerate(individual.chromosome)if x==1]
#     while coverage_set:
#         upstream_nodes = [i[0] for i in temp_Gsub.in_degree() if i[1] == 0]
#         for i in upstream_nodes:
#             # print(i)
#             # print(temp_Gsub.nodes())
#             temp_Gsub.remove_node(i)
#             temp_set = coverage_set.intersection(individual.upstream_set[i])
#             length=len(temp_set)
#
#             additional_upstream[i] = len(temp_set)
#             additional_upset[i] = temp_set
#
#             coverage_set = coverage_set.difference(individual.upstream_set[i])
#     temp_Gsub = individual.Gsub.copy()
#     down_nodes = [i[0] for i in temp_Gsub.out_degree() if i[1] == 0]
#
#     while len(down_nodes):
#         for i in down_nodes:
#             down_nodes.remove(i)
#             upstream_bunch = additional_upset[i]
#             for j in temp_positive_manholes:
#                 if j in upstream_bunch:
#                     #                 print('add',j)
#                     upstream_bunch = upstream_bunch | additional_upset[i]
#             intersect = upstream_bunch.intersection(temp_positive_manholes)
#             bunch_len = len(upstream_bunch)
#             for j in intersect:
#                 search_cost += len(additional_upset[j]) / bunch_len * math.log(len(additional_upset[j]), 2)
#     # print(search_cost)
#     if sum(individual.chromosome)==0:
#         search_cost=0
#     else:
#         search_cost=search_cost/sum(individual.chromosome)
#     # print(search_cost)
#     return search_cost

#
# @profile
# def new_search_cost_by_topology(problem,individual):
#
#     # print('upstram,',len(problem.upstream_set))
#     if np.sum(individual.chromosome)==0:
#             search_cost=0
#     else:
#         coverage_set=individual.coverage_set
#         temp_Gsub=individual.Gsub.copy()
#
#         # 首先计算additional upstream
#         additional_upstream = {}
#         # temp_positive_manholes = np.array(np.where(individual.chromosome==1 ))[0].tolist()
#
#         while coverage_set:
#             upstream_nodes = [i[0] for i in temp_Gsub.in_degree() if i[1] == 0]
#             for i in upstream_nodes:
#                 temp_set = coverage_set.intersection(problem.upstream_set[i])
#                 length=len(temp_set)
#
#                 additional_upstream[i] = len(temp_set)
#                 # coverage_set1 = coverage_set.difference(problem.upstream_set[i])
#                 coverage_set.difference_update(problem.upstream_set[i])
#                 temp_Gsub.remove_node(i)
#
#
#         # 然后分bunch计算
#
#         # 首先转为undirected计算不连通的子集
#         undirected_Gsub = individual.Gsub.to_undirected()
#         nodeSet = []
#         for c in nx.connected_components(undirected_Gsub):
#             # 得到不连通的子集
#             # nodeSet.append(list(undirected_Gsub.subgraph(c).nodes()))
#             nodeSet.append(set(undirected_Gsub.subgraph(c).nodes()))
#
#         temp_Gsub = individual.Gsub.copy()
#         upstream_nodes = [i[0] for i in temp_Gsub.in_degree() if i[1] == 0]
#
#         bunch_dict={}
#         cnt=0
#         bunch_coverage={}
#         while len(upstream_nodes):
#             i = upstream_nodes[0]
#             upstream_nodes.remove(i)
#             ancestor = problem.upstream_set[i]
#             bunch_dict[cnt] = []
#             bunch_dict[cnt].append(i)
#             #     bunch_coverage[cnt]=set()
#             bunch_coverage[cnt] = problem.upstream_set[i]
#             temp_ancestor = ancestor
#
#             nodeSet_i=[set for set in nodeSet if i in set][0]
#             common_upstream=[_ for _ in nodeSet_i if _ in upstream_nodes]
#             for _ in common_upstream:
#                 upstream_nodes.remove(_)
#
#             # while len(upstream_nodes):
#             for j in upstream_nodes:
#                 temp_ancestor = temp_ancestor.intersection(problem.upstream_set[j])
#
#                 if len(temp_ancestor) != 0:
#                     # upstream_nodes.remove(j)
#                     bunch_dict[cnt].append(j)
#                     # bunch_coverage[cnt].update(problem.upstream_set[j])
#                     bunch_coverage[cnt] = bunch_coverage[cnt] | problem.upstream_set[j]
#
#
#             # upstream_nodes
#             for k in bunch_dict[cnt]:
#                 if k in upstream_nodes:
#                     upstream_nodes.remove(k)
#             cnt += 1
#         # print('bunch_dict', bunch_dict)
#         # print(len(bunch_dict))
#         search_cost = 0
#         for i in range(cnt):
#             bunch_size = len(bunch_coverage[i])
#
#             for k in nodeSet:
#                 if k.intersection(bunch_dict[i]):
#                 # if set(k).intersection(bunch_dict[i]):
#                 #     bunch_dict[i] = set(bunch_dict[i]) | set(k)
#                     bunch_dict[i] = set(bunch_dict[i]) | k
#
#             for j in bunch_dict[i]:
#                 search_cost += math.log(additional_upstream[j], 2) * additional_upstream[j] / bunch_size
#         search_cost=search_cost/np.sum(individual.chromosome)
#
#     return search_cost

# @profile
# this is the final edition




# @profile
# def search_cost_arr(problem,individual):
#     if np.sum(individual.chromosome)==0:
#         return 0
#     elif np.sum(individual.chromosome)==1:
#         i=individual.positive_nodes[0]
#         search_cost=math.log(problem.upstream_arr[i],2)
#         return search_cost
#     else:
#
#         # 开始search cost 计算
#
#         # 首先计算additional search cost
#         additional_upstream = {}
#         temp_coverage_set = individual.coverage_set.copy()
#         temp_sub_connectivity = individual.sub_conn.copy()
#         temp_positive_manholes = individual.positive_nodes.copy()
#
#         loopcnt=0
#         while len(temp_positive_manholes):
#         # while(temp_sub_connectivity.any()):
#             temp_upstream_nodes = [i for i in temp_positive_manholes if np.sum(temp_sub_connectivity[:, i]) == 0]
#             if  len(temp_upstream_nodes)==0:
#                 temp_upstream_nodes=temp_positive_manholes
#
#             for i in temp_upstream_nodes:
#                 temp_positive_manholes.remove(i)
#                 temp_sub_connectivity[i, :] = 0
#                 temp_set = temp_coverage_set.intersection(problem.upstream_set[i])
#                 # temp_coverage_set = temp_coverage_set.difference(problem.upstream_set[i])
#                 temp_coverage_set=temp_coverage_set.difference(temp_set)
#                 length = len(temp_set)
#                 if length>1:
#                     additional_upstream[i] = length
#                 else:
#                     additional_upstream[i]=1
#                 # print('after',temp_coverage_set)
#
#
#
#         positive_manholes=individual.positive_nodes.copy()
#         upstream_nodes = [i for i in positive_manholes if np.sum(individual.sub_conn[:, i]) == 0]
#
#         cnt = 0
#         nodeSet = []
#         for i in upstream_nodes:
#             # print('stuck 2')
#             list_i = [k for k in positive_manholes if individual.sub_conn[i, k]]
#             nodeSet.append(list_i)
#             nodeSet[cnt].append(i)
#             cnt += 1
#
#
#         bunch_dict = {}
#         bunch_coverage = {}
#         cnt = 0
#
#
#
#
#         while len(upstream_nodes):
#             # print('stuck 3')
#             i = upstream_nodes[0]
#             upstream_nodes.remove(i)
#             ancestor = problem.upstream_set[i]
#             bunch_dict[cnt] = []
#             bunch_dict[cnt].append(i)
#             bunch_coverage[cnt] = problem.upstream_set[i]
#             temp_ancestor = ancestor
#             for j in upstream_nodes.copy():
#                 temp_ancestor = temp_ancestor.intersection(problem.upstream_set[j])
#                 if len(temp_ancestor) != 0:
#                     # upstream_nodes.remove(j)
#                     bunch_dict[cnt].append(j)
#                     bunch_coverage[cnt] = bunch_coverage[cnt] | problem.upstream_set[j]
#             for k in bunch_dict[cnt]:
#                 if k in upstream_nodes:
#                     upstream_nodes.remove(k)
#             cnt += 1
#         # print('bunch_dict',bunch_dict)
#         # print(len(bunch_dict))
#         # print('c',bunch_coverage)
#         search_cost = 0
#         for i in range(cnt):
#             bunch_size = len(bunch_coverage[i])
#
#             for k in nodeSet:
#                 if set(k).intersection(bunch_dict[i]):
#                     bunch_dict[i] = set(bunch_dict[i]) | set(k)
#
#             for j in bunch_dict[i]:
#                 # print(bunch_dict[i])
#                 # print(j,additional_upstream)
#                 if j not in additional_upstream.keys():
#                     additional_upstream[j]=problem.upstream_arr[j]
#                     print(additional_upstream[j])
#                 search_cost += math.log(additional_upstream[j], 2) * additional_upstream[j] / bunch_size
#         search_cost = search_cost / np.sum(individual.chromosome)
#
#         return search_cost


# def final_edition_search_cost(problem, individual):
#     if np.sum(individual.chromosome) == 0:
#         search_cost = 0
#     else:
#
#         # 首先转为undirected计算不连通的子集
#         undirected_Gsub = individual.Gsub.to_undirected()
#         # nodeSet = []
#         # for c in nx.connected_components(undirected_Gsub):
#         #     # 得到不连通的子集
#         #     # nodeSet.append(list(undirected_Gsub.subgraph(c).nodes()))
#         #     nodeSet.append(set(undirected_Gsub.subgraph(c).nodes()))
#         nodeSet = [set(undirected_Gsub.subgraph(c).nodes()) for c in nx.connected_components(undirected_Gsub)]
#
#         coverage_set = individual.coverage_set
#         coverage = len(coverage_set)
#         temp_Gsub = individual.Gsub
#         search_cost = 0
#
#         # 首先计算additional upstream
#         additional_upstream = {}
#         # temp_positive_manholes = np.array(np.where(individual.chromosome==1 ))[0].tolist()
#
#         while coverage_set:
#             upstream_nodes = [i[0] for i in temp_Gsub.in_degree() if i[1] == 0]
#             for i in upstream_nodes:
#                 temp_set = coverage_set.intersection(problem.upstream_set[i])
#                 length = len(temp_set)
#
#                 additional_upstream[i] = len(temp_set)
#                 # coverage_set1 = coverage_set.difference(problem.upstream_set[i])
#                 coverage_set.difference_update(problem.upstream_set[i])
#                 temp_Gsub.remove_node(i)
#
#         for component in nodeSet:
#             temp_coverage_set = set()
#             for node in component:
#                 temp_coverage_set.update(problem.upstream_set[node])
#                 # temp_coverage_set=temp_coverage_set|problem.upstream_set[node]
#             bunch_size = len(temp_coverage_set)
#             for node in component:
#                 if node in additional_upstream and additional_upstream[node] > 0:
#                     search_cost += math.log(additional_upstream[node], 2) * additional_upstream[node] / coverage
#         # search_cost=search_cost/np.sum(individual.chromosome)
#
#     return search_cost
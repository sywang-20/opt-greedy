import networkx as nx
import pickle
import matplotlib.pyplot as plt
from population import Population
from individual import Individual
import numpy as np

# G=nx.read_gpickle('./100/prepared/syn.pkl')
# with open('./100/prepared/pos.pkl','rb') as f:
#     pos=pickle.load(f)
# for i in range(2):
#     print(i)
#     print(list(G.to_undirected().neighbors(i)))
#     print(list(G.neighbors(i)))
# nx.draw(G,pos,with_labels=True)
# plt.show()

with open('./test/solution.pkl','rb') as f:
    solution=pickle.load(f)

last=solution[len(solution)-1]
# print(len(solution))
# print(solution[len(solution)-1])
# print(len(solution[3]))
obj1=[i[0] for i in last]
obj2=[i[1] for i in last]
obj3=[i[2] for i in last]
print(np.average(obj1))

print(np.average(obj2))
print(np.average(obj3))

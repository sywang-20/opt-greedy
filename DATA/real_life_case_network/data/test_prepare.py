import networkx as nx
import pickle
from nsga import precomputation
def cal_upstream_link(G,node):
    print('for each node')

def generate_upstream_link(G):
    print('for whole graph')
if __name__=='__main__':
    fn='E:/sewage-sensor-placement/extract_topo_graph/data/pipe_TM.shp'

    G=nx.read_shp(fn)

    print('edge len1',len(G.edges()))
    G.remove_edge((815783.0579000004, 828304.5431999993), (815786.0312999999, 828303.9664999992))
    print('edge len2', len(G.edges()))

    numNodes = len(G.nodes())
    labels_before = list(G.nodes)
    labels_after = list(range(numNodes))
    mapping = dict(zip(labels_before, labels_after))
    print(mapping)

    H=nx.DiGraph()

    G = nx.relabel_nodes(G, mapping)
    # print(H.edges())

    upstream_arr, upstream_set = precomputation.generate_upstream_arr_from_node(G)


    with open("./prepared/upstream_arr.pkl", "wb") as tf:
        pickle.dump(upstream_arr, tf,protocol=3)

    with open("./prepared/upstream_set.pkl", "wb") as tf:
        pickle.dump(upstream_set, tf,protocol=3)

    tf.close()

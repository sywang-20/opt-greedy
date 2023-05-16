import networkx as nx
import pickle
from nsga import precomputation
if __name__=='__main__':
    fn='E:/sewage-sensor-placement/extract_topo_graph/data/pipe_TM.shp'

    G=nx.read_shp(fn)

    # there is a loop(2029,2030),(2030,2029)
    # G = nx.read_gpickle(filename)

    # precomputation: 用重新编号的图H代替原来的图


    print('edge len1',len(G.edges()))
    G.remove_edge((815783.0579000004, 828304.5431999993), (815786.0312999999, 828303.9664999992))
    print('edge len2', len(G.edges()))

    numNodes = len(G.nodes())
    labels_before = list(G.nodes)
    labels_after = list(range(numNodes))
    mapping = dict(zip(labels_before, labels_after))
    print(mapping)

    H=nx.DiGraph()

    H = nx.relabel_nodes(G, mapping)
    # print(H.edges())

    nx.write_gpickle(H,'./prepared/pipe_TM_clean_relabel.pkl',protocol=3)
    # print(H.edges[933])

    with open("./prepared/label_mapping.pkl", "wb") as tf:
        pickle.dump(mapping, tf,protocol=3)

    upstream_arr, upstream_set = precomputation.generate_upstream_arr_from_node(H)
    # print(upstream_set)
    # print(upstream_arr)

    with open("./prepared/upstream_arr.pkl", "wb") as tf:
        pickle.dump(upstream_arr, tf,protocol=3)

    with open("./prepared/upstream_set.pkl", "wb") as tf:
        pickle.dump(upstream_set, tf,protocol=3)

    tf.close()

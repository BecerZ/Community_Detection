import networkx as nx
import matplotlib.pyplot as plt

def readGML(path):
    g = nx.read_gml(path, label="id")
    return g

def readTxt(path):
    df = pd.read_csv(path, sep=" ", header=None)
    return df
def calculateEdgeBetweenness(G):
    edge_betweenness_list = {x:0 for x in G.edges()}
    total_number_of_paths = 0
    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                shortest_paths = nx.shortest_path(G, source, target)
                total_number_of_paths = total_number_of_paths + len(shortest_paths)
                for node_source in shortest_paths:
                    for node_target in shortest_paths:
                        if node_source != node_target:
                            if G.has_edge(node_source, node_target):
                                try:
                                    edge_betweenness_list[(node_source,node_target)] += 1
                                except(KeyError):
                                    continue

    for c in edge_betweenness_list:
        edge_betweenness_list[c] = edge_betweenness_list[c] / total_number_of_paths

    return edge_betweenness_list

def edge_to_remove(G):
    dict = calculateEdgeBetweenness(G)
    list_of_tuples = dict.items()
    list_of_tuples = sorted(list_of_tuples, key=lambda x: x[1], reverse=True)
    removed_edge = list_of_tuples[0][0]
    return removed_edge

def GirvanNewman(G):
    c = nx.connected_component_subgraphs(G)
    length_c = nx.number_connected_components(G)
    #continue until the graph is empty
    while(length_c == 1):
        G.remove_edge(*edge_to_remove(G))
        c= nx.connected_component_subgraphs(G)
        length_c = nx.number_connected_components(G)
    return c

def main():
    path1 = "C:\\Users\\Bora\\Desktop\\ALL SHITS\\Bilkent\\4. Senior Year\\CS425\\Project\\facebook_combined.txt\\facebook_combined.txt"
    path2 = "C:\\Users\\Bora\\Desktop\\ALL SHITS\\Bilkent\\4. Senior Year\\CS425\\Project\\karate\\karate.gml"
    g = readGML(path2)
    print(nx.info(g))
    c = GirvanNewman(g)
    counter = 1
    for i in c:
        print("community: ", counter, i.nodes())
        counter += 1

main()
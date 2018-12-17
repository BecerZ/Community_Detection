import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def readGML(path):
    g = nx.read_gml(path, label="id")
    return g

def readTxt(path):
    g = nx.read_edgelist(path, delimiter=" ")
    return g

def calculateEdgeBetweenness(G):
    edge_betweenness_list = {x:0 for x in G.edges()}
    total_number_of_paths = 0
    for source in G.nodes():
        for target in G.nodes():
            if source != target:
                if nx.has_path(G, source, target):
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
                else:
                    continue
    for c in edge_betweenness_list:
        edge_betweenness_list[c] = edge_betweenness_list[c] / total_number_of_paths
    return edge_betweenness_list

def edge_to_remove(G):
    dict = calculateEdgeBetweenness(G)
    list_of_tuples = dict.items()
    list_of_tuples = sorted(list_of_tuples, key=lambda x: x[1], reverse=True)
    removed_edges = []
    for (i, v) in list_of_tuples:
        if v == list_of_tuples[0][1]:
            removed_edges.append(i)
    return removed_edges

def calculateModularity(G, communities):
    modularity = 0
    edge_amount = len(G.edges())
    for community in communities:
        degree_list = [(node, val) for (node, val) in community.degree()]
        for i in degree_list:
            source = i[0]
            source_degree = i[1]
            for j in degree_list:
                target = j[0]
                target_degree = j[1]
                if source != target:
                    if (source,target) in community.edges():
                        modularity += (1-((source_degree*target_degree)/(2*edge_amount)))
    modularity = modularity / (2*edge_amount) #normalization
    return modularity

def GirvanNewman(G):
    removed_edges = []
    partition = nx.connected_component_subgraphs(G)
    g_copy = G.copy()
    length_components = nx.number_connected_components(g_copy)
    while length_components == 1:
        edges_to_remove = edge_to_remove(g_copy)
        for e in edges_to_remove:
            g_copy.remove_edge(*e)
        communities = nx.connected_component_subgraphs(g_copy)
        curr_modularity = calculateModularity(G, communities)
        if curr_modularity < 0.5:
            break
        else:
            partition = nx.connected_component_subgraphs(g_copy)
        removed_edges.extend(edges_to_remove)
        length_components = nx.number_connected_components(g_copy)
    return partition, removed_edges
"""
def GirvanNewman(G):
    c = nx.connected_component_subgraphs(G)
    length_c = nx.number_connected_components(G)
    removed_edges = {}
    #continue until the graph is empty
    level_counter = 1
    while(length_c == 1):
        edges = edge_to_remove(G)
        for e in edges:
            removed_edges.update({e:level_counter})
            level_counter += 1
            G.remove_edge(*e)
        c= nx.connected_component_subgraphs(G)
        length_c = nx.number_connected_components(G)
    return c, removed_edges
"""
def plot_graph(G,communities, removed_edges, node_size, fb_flag):
    #Fb_flag = 0 for small dataset, 1 for large dataset
    if fb_flag == 0:
        pos = nx.spring_layout(G, k=1.1, iterations=100, scale=5)
    else:
        pos = nx.spring_layout(G)
    colors = ["r", "g"]
    counter = 0
    f = plt.figure(1)
    for i in communities:
        nx.draw_networkx_nodes(G, pos=pos, nodelist=list(i.nodes()), node_color=colors[counter],node_size=node_size, alpha=1)
        counter += 1
        nx.draw_networkx_edges(G, pos=pos, edgelist=i.edges(), width=2, alpha=1, edge_color='k')
    if fb_flag == 0:
        nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
        nx.draw_networkx_edges(G, pos=pos, edgelist=removed_edges, width=2, alpha=1, edge_color='k', style="dashed")
    plt.axis('off')
    plt.show()

def main():
    path1 = "C:\\Users\\Bora\\Desktop\\ALL SHITS\\Bilkent\\4. Senior Year\\CS425\\Project\\facebook_combined.txt\\facebook_combined.txt"
    path2 = "C:\\Users\\Bora\\Desktop\\ALL SHITS\\Bilkent\\4. Senior Year\\CS425\\Project\\karate\\karate.gml"
    ##Karate Dataset
    G = readGML(path2)
    print(nx.info(G))
    partition, removed_edges = GirvanNewman(G)
    plot_graph(G, partition, removed_edges, 500, 0)
    ##Facebook dataset
    G_1 = readTxt(path1)
    print(nx.info(G_1))
    pos = nx.spring_layout(G_1)
    nx.draw_networkx(G_1, pos=pos, with_labels=False, node_size=35)
    partition_fb, removed_edges_fb = GirvanNewman(G_1)
    plot_graph(G_1, removed_edges, 35, 1)
    plt.show()
main()
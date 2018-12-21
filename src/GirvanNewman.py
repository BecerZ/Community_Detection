import networkx as nx
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
import numpy as np
import random
from collections import deque
def readGML(path):
    g = nx.read_gml(path, label="id")
    return g

def readTxt(path):
    g = nx.read_edgelist(path, delimiter=" ")
    return g

def calculateEdgeBetweennessBrandes(G):
    vertex_set = G.nodes()
    betweenness = dict.fromkeys(G, 0.0)
    betweenness.update(dict.fromkeys(G.edges(), 0.0))
    for vertex in vertex_set:
        S = []
        P = dict((w, []) for w in vertex_set)
        sigma = dict((t, 0) for t in vertex_set)
        sigma[vertex] = 1
        d = dict((t, -1) for t in vertex_set)
        d[vertex] = 0
        Q = deque([])
        Q.append(vertex)
        while Q:
            v = Q.popleft()
            S.append(v)
            for neighbor in G.neighbors(v):
                if d[neighbor] < 0:
                    Q.append(neighbor)
                    d[neighbor] = d[v] + 1
                if d[neighbor] == d[v] + 1:
                    sigma[neighbor] = sigma[neighbor] + sigma[v]
                    P[neighbor].append(v)
        delta = dict.fromkeys(S, 0)
        while S:
            w = S.pop()
            coeff = (1 + delta[w]) / sigma[w]
            for v in P[w]:
                c = sigma[v] * coeff
                if (v, w) not in betweenness:
                    betweenness[(w,v)] += c
                else:
                    betweenness[(v,w)] += c
                delta[v] += c
                if w != vertex:
                    betweenness[w] += delta[w]
    for n in G:
        del betweenness[n]
    return betweenness

def calculateEdgeBetweennessNaive(G):
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
    dict = calculateEdgeBetweennessBrandes(G)
    list_of_tuples = dict.items()
    list_of_tuples = sorted(list_of_tuples, key=lambda x: x[1], reverse=True)
    return list_of_tuples[0][0]

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

def GirvanNewman(G, community_count):
    removed_edges = []
    partition = nx.connected_component_subgraphs(G)
    g_copy = G.copy()
    length_components = nx.number_connected_components(g_copy)
    while length_components <= community_count:
        to_remove = edge_to_remove(g_copy)
        g_copy.remove_edge(*to_remove)
        partition = nx.connected_component_subgraphs(g_copy)
        removed_edges.extend(to_remove)
        length_components = nx.number_connected_components(g_copy)
    return partition, removed_edges

def plot_graph_large_ds(G,communities, figure_no):
    pos = nx.spring_layout(G)
    colors = ["r", "g"]
    counter = 0
    f = plt.figure(figure_no)
    for i in communities:
        nx.draw_networkx_nodes(G, pos=pos, nodelist=list(i.nodes()), node_color=colors[counter],node_size=node_size, alpha=1)
        nx.draw_networkx_edges(G, pos=pos, edgelist=i.edges(), width=2, alpha=1, edge_color='k')
        counter += 1
    plt.axis('off')

def plot_graph_small_ds(G,communities, node_size, figure_no):
    #Fb_flag = 0 for small dataset, 1 for large dataset
    pos = nx.spring_layout(G, k=1.1, iterations=100, scale=5)
    counter = 0
    f = plt.figure(figure_no)
    colors = ["r", "g", "c", "b", "y", "g", "b"]
    for i in communities:
        if i.edges():
            if counter == 7 or counter == 6:
                nx.draw_networkx_nodes(G, pos=pos, nodelist=list(i.nodes()), node_color=colors[counter], node_size=node_size,alpha=0.5)
                nx.draw_networkx_edges(G, pos=pos, edgelist=i.edges(), width=2, alpha=1, edge_color='k')
            else:
                nx.draw_networkx_nodes(G, pos=pos, nodelist=list(i.nodes()), node_color=colors[counter],node_size=node_size, alpha=1)
                nx.draw_networkx_edges(G, pos=pos, edgelist=i.edges(), width=2, alpha=1, edge_color='k')
            counter += 1
        else:
            nx.draw_networkx_nodes(G, pos=pos, nodelist=list(i.nodes()), node_color='w', node_size=node_size,alpha=1)
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')
    plt.axis('off')

def main():
    path1 = "D:\\Users\\Bora\\Desktop\\ALL SHITS\\Bilkent\\4. Senior Year\\CS425\\Project\\facebook_combined.txt\\facebook_combined.txt"
    path2 = "D:\\Users\\Bora\\Desktop\\ALL SHITS\\Bilkent\\4. Senior Year\\CS425\\Project\\karate\\karate.gml"
    ##Karate Dataset
    G = readGML(path2)
    print(nx.info(G))
    nodes_size = len(G.nodes())
    #partition, removed_edges = GirvanNewman(G, 1)
    #plot_graph_small_ds(G, partition, 500, 1)
    for i in range(nodes_size):
        if i == 0:
            continue
        else:
            partition, removed_edges = GirvanNewman(G, i)
            plot_graph_small_ds(G, partition, 500,i)
    plt.show()
    ##For large datasets, use GirvanNewman(G, 1) this will return 2 highest level communities
    """
    ##Facebook dataset
    G_1 = readTxt(path1)
    print(nx.info(G_1))
    pos = nx.spring_layout(G_1)
    nx.draw_networkx(G_1, pos=pos, with_labels=False, node_size=35)
    partition_fb, removed_edges_fb = GirvanNewman(G_1)
    plot_graph(G_1, removed_edges, 35, 1)
    """
main()
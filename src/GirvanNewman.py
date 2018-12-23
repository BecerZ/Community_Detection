import networkx as nx
import matplotlib.pyplot as plt
import time
from collections import deque
import warnings
warnings.filterwarnings('ignore')

def thread_time_experiment():
    thread_counts = [1, 2, 4, 8]
    ds_1 = [1.966, 1.088, 0.755, 0.552]
    ds_2 = [39.506, 20.88, 12.661, 11.486]
    ds_3 = [613.065, 318.05, 200.447, 161.122]
    ds_4 = [3206.39, 1750.63, 1126.12, 1030.27]
    ds_fb = [1119.22, 567.387, 312.696, 281.434]
    f = plt.figure(1)
    plt.xlabel('thread count')
    plt.ylabel('seconds')
    plt.plot(thread_counts, ds_1, color='red', label='dataset 1', linewidth=2)
    plt.plot(thread_counts, ds_2, color='green', label='dataset 2', linewidth=2)
    plt.plot(thread_counts, ds_3, color='cyan', label='dataset 3', linewidth=2)
    plt.plot(thread_counts, ds_4, color='magenta', label='dataset 4', linewidth=2)
    plt.plot(thread_counts, ds_fb, color='blue', label='fb dataset', linewidth=2)
    legend = plt.legend(loc='upper right', ncol=1)
    plt.show()

def readGraphml(path):
    g = nx.read_graphml(path)
    return g

def readGML(path):
    g = nx.read_gml(path, label="id")
    return g

def readTxt(path):
    g = nx.read_edgelist(path, delimiter=" ")
    return g

def writeTxt(path):
    out = open(path, 'w')
    for e in G.edges():
        print(e[0])
        line = str(e[0]) + " " + str(e[1])
        out.write(line)
        out.write("\n")


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
            for v in P[w]:
                c = sigma[v] /sigma[w]
                c = c *(1 + delta[w])
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

def plot_original(G, figure_no):
    pos = nx.spring_layout(G)
    f = plt.figure(figure_no)
    nx.draw(G, pos=pos, node_size=10, node_color ="g")
    plt.axis('off')
def plot_graph_large_ds(G,communities,figure_no):
    pos = nx.spring_layout(G)
    colors = ["r", "g", "c", "b", "y", "g", "b"]
    counter = 0
    f = plt.figure(figure_no)
    for i in communities:
        nx.draw_networkx_nodes(G, pos=pos, nodelist=list(i.nodes()), node_color=colors[counter],node_size=10, alpha=1)
        nx.draw_networkx_edges(G, pos=pos, edgelist=i.edges(), width=2, alpha=1, edge_color='k')
        counter += 1
    plt.axis('off')

def plot_graph_small_ds(G,communities, node_size, figure_no):
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
    path = "..\\processed_v2\\15.txt"
    G = readTxt(path3)
    print(nx.info(G))

    start = time.time()
    for i in range(3):
        if i == 0:
            continue
        else:
            partition, removed_edges = GirvanNewman(G, i)
            plot_graph_large_ds(G, partition, i)
    end = time.time()
    print("Elapsed Time In Seconds:", end-start)
    plot_original(G, 4)
    plt.show()

if __name__== '__main__':
    main()
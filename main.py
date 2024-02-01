import networkx as nx
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

G = nx.read_edgelist('web-Stanford.txt', create_using=nx.DiGraph)

dangling_nodes = [node for node in G.nodes() if G.out_degree(node) == 0]
while dangling_nodes:
    G.remove_nodes_from(dangling_nodes)
    dangling_nodes = [node for node in G.nodes() if G.out_degree(node) == 0]

# Identify the largest weakly connected component
largest_wcc = max(nx.weakly_connected_components(G), key=len)
wcc_subgraph = G.subgraph(largest_wcc)
print("Largest Weakly Connected Component:")
print("Number of nodes:", wcc_subgraph.number_of_nodes())
print("Number of edges:", wcc_subgraph.number_of_edges())
pagerank_wcc = nx.pagerank(wcc_subgraph)
with open("pagerank_wcc.txt", "w") as f:
    for node, score in pagerank_wcc.items():
        f.write(f"{node}\t{score}\n")

largest_scc = max(nx.strongly_connected_components(G), key=len)
scc_subgraph = G.subgraph(largest_scc)
print("\nLargest Strongly Connected Component:")
print("Number of nodes:", scc_subgraph.number_of_nodes())
print("Number of edges:", scc_subgraph.number_of_edges())

pagerank_scc = nx.pagerank(scc_subgraph)
with open("pagerank_scc.txt", "w") as f:
    for node, score in pagerank_scc.items():
        f.write(f"{node}\t{score}\n")


randgraph = nx.fast_gnp_random_graph(n=wcc_subgraph.number_of_nodes(), p=0.00008, directed=False)
pagerank_randgraph = nx.pagerank(randgraph)
with open("pagerank_randgraph.txt", "w") as f:
    for node, score in pagerank_randgraph.items():
        f.write(f"{node}\t{score}\n")

original_wcc_edges = wcc_subgraph.number_of_edges()
m = int(original_wcc_edges / wcc_subgraph.number_of_nodes()) + 1
print(f"\nAppropriate m value for Barabasi-Albert Graph: {m}")

bagraph = nx.barabasi_albert_graph(n=wcc_subgraph.number_of_nodes(), m=m, seed=1)
pagerank_bagraph = nx.pagerank(bagraph)

with open("pagerank_bagraph.txt", "w") as f:
    for node, score in pagerank_bagraph.items():
        f.write(f"{node}\t{score}\n")


pagerank_original = nx.pagerank(wcc_subgraph)


sorted_nodes_original = sorted(pagerank_original, key=pagerank_original.get, reverse=True)
sorted_nodes_rand = sorted(pagerank_randgraph, key=pagerank_randgraph.get, reverse=True)
sorted_nodes_ba = sorted(pagerank_bagraph, key=pagerank_bagraph.get, reverse=True)

values_original = np.array([pagerank_original[node] for node in sorted_nodes_original])
randgr_values = np.array([pagerank_randgraph[node] for node in sorted_nodes_rand])
ba_values = np.array([pagerank_bagraph[node] for node in sorted_nodes_ba])

values_original = values_original.reshape(1, -1)
randgr_values = randgr_values.reshape(1, -1)
ba_values = ba_values.reshape(1, -1)

cosine_sim_random = cosine_similarity(values_original, randgr_values)[0, 0]
cosine_sim_barabasi = cosine_similarity(values_original, ba_values)[0, 0]

print("\nCosine Similarity with Random Graph:", cosine_sim_random)
print("Cosine Similarity with Barabasi-Albert Graph:", cosine_sim_barabasi)


def draw_top_k(graph, pagerank_scores, k):
    top_k_nodes = sorted(graph.nodes(), key=pagerank_scores.get, reverse=True)[:k]
    subgraph = graph.subgraph(top_k_nodes)
    pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=True, node_size=300, font_size=8, font_color='black', font_weight='bold')
    plt.title(f"Top-{k} Nodes by PageRank")
    plt.show()


k = 100
draw_top_k(wcc_subgraph, pagerank_wcc, k)
draw_top_k(randgraph, pagerank_randgraph, k)
draw_top_k(bagraph, pagerank_bagraph, k)

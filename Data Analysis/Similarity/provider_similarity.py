import numpy as np
import pandas as pd
import csv, sys
from html_similarity import structural_similarity, style_similarity
import networkx as nx
import matplotlib.pyplot as plt
from sklearn import cluster
from sklearn.cluster import DBSCAN
from IPython.display import display
from functools import cache
from datetime import datetime

# How similar are inboxes?
# Load html from csv file

csvInputFile = open("Data Analysis/Similarity/inbox_html.csv", "r", newline="", encoding="utf-8")
csvInputReader = csv.reader(csvInputFile)
# Skip Header
next(csvInputReader)

# Needed to process large csv cells without error
maxInt = sys.maxsize
while True:
    # decrease the maxInt value by factor 10
    # as long as the OverflowError occurs.

    try:
        csv.field_size_limit(maxInt)
        break
    except OverflowError:
        maxInt = int(maxInt/10)


providers = []
htmls = []
for row in csvInputReader:
    # Build list of providers and html
    providers += [row[0]]
    htmls += [row[2]]

# Slice for testing
#providers = providers[:10]

# Calculate similarity matrix
A = np.empty(shape=(len(providers), len(providers)))        # Create empty array
print(A)
k = 0.3     # 0.3 Recommended
# Iterate through providers
for i, providerA in enumerate(providers):
    # For each provider compare with each other provider with index >= i
    for j, providerB in enumerate(providers):
        if j < i:
            continue    # Skip provider, since already compared before
        # Calculate similarity
        similarity = k * structural_similarity(htmls[i], htmls[j]) + (1 - k) * style_similarity(htmls[i], htmls[j])
        # Save into array
        A[i, j] = similarity
        A[j, i] = similarity
        print("Compare %s and %s: %0.05f" % (providerA, providerB, similarity))
print(A)

# Convert to pandas data frame
df = pd.DataFrame(A, columns=providers, index=providers)
print(df)

# Create graph from similarity matrix with similarity as weight
G = nx.from_numpy_array(A)
print(G)

# Remove self-loop edges
G.remove_edges_from(nx.selfloop_edges(G))

# Cluster data

# Distance matrix: 1 - similarity
B = 1 - A
print(B)

# EPS Value, threshold for neighbour decision
eps = 0.8
clustering = DBSCAN(metric="precomputed", eps=eps, min_samples=2).fit(B)
print('Cluster labels:', clustering.labels_)
clusters = clustering.labels_

# Plot size
plt.figure(figsize=(11.7, 8.3))
# Draw graph
pos = nx.spring_layout(G, seed=7)  # positions for all nodes - seed for reproducibility
# nodes
nx.draw_networkx_nodes(G, pos, node_color=clustering.labels_, cmap=plt.cm.Set2)
# edges
# color edges below cluster threshold
edges = [(u, v, d) for (u, v, d) in G.edges(data=True) if d["weight"] > (1-eps)]
nx.draw_networkx_edges(G, pos, edgelist=edges, alpha=0.4)
# labels for nodes
node_labels = {i: providers[i] for i, v in enumerate(providers)}
nx.draw_networkx_labels(G, pos, labels=node_labels, verticalalignment="top", font_size=6)
# labels for edges
edge_labels = {(u, v): "{:.2f}".format(d['weight']) for (u, v, d) in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=4)

plt.show()

# Generate list of Clusters and save to csv
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csvOutputFile = open(f"Data Analysis\Similarity\clusters_{timestamp}.csv", "w", newline="", encoding="utf-8")
csvOutputWriter = csv.writer(csvOutputFile)
# Header
csvOutputWriter.writerow(['cluster', 'host'])

clustered_providers = list(zip(providers, clusters))
for i in range(min(clusters), max(clusters)):
    cluster_members = [provider for (provider, cluster_name) in clustered_providers if cluster_name == i]
    print(f'Cluster {i} with ({len(cluster_members)}) members:')
    for cluster_member in cluster_members:
        print(cluster_member)
        csvOutputWriter.writerow([i, cluster_member])
csvOutputFile.close()

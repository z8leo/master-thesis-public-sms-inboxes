import csv
from random import seed
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

CLUSTERS_FILE = 'Data\Characteristics\clusters_20220505_104537.csv'
NUMBERS_PROVIDERS_FILE = 'Data/Characteristics/numbers_per_provider_2022_09_22.csv'

# Get Cluster numbers
with open(CLUSTERS_FILE, mode='r') as file:
    reader = csv.reader(file)
    cluster_dict = {row[1]:row[0] for row in reader}

csvInputFile = open(NUMBERS_PROVIDERS_FILE, "r", newline="", encoding="utf-8")
csvInputReader = csv.reader(csvInputFile)
# Skip Header
next(csvInputReader)

providers = []
numbers = []
totals = []
shared = []
clusters = []
for row in csvInputReader:
    # Build list of providers and html
    providers += [row[0]]
    totals += [row[1]]
    number_list = row[2].split(',')
    numbers += [number_list]   # Convert to list
    clusters += [int(cluster_dict.get(row[0], '-1'))]



# Calculate similarity matrix
A = np.empty(shape=(len(providers), len(providers)))        # Create empty array
#print(A)
# Iterate through providers
for i, providerA in enumerate(providers):
    # For each provider compare with each other provider with index >= i
    for j, providerB in enumerate(providers):
        if j < i:
            continue    # Skip provider, since already compared before
        # Get list of numbers that are shared between providerA and providerB
        shared_list = [shared for shared in numbers[i] if shared in numbers[j]]
        # Save into array
        A[i, j] = len(shared_list)
        A[j, i] = len(shared_list)
        print("Compare %s and %s: %0i" % (providerA, providerB, len(shared_list)))
        # Append to list if shared between to different providers
        if i != j:
            shared += shared_list

print(A)

# Reduce shared number list to unique values
unique_shared = np.unique(np.array(shared))
print(len(unique_shared), unique_shared[:10])
# Save to csv file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csvOutputFile = open(f"Data Analysis\Shared Numbers\shared_numbers_unique_{timestamp}.csv", "w", newline="", encoding="utf-8")
csvOutputWriter = csv.writer(csvOutputFile)
for number in unique_shared:
    csvOutputWriter.writerow([number])
csvOutputFile.close()

# Convert to pandas data frame
df = pd.DataFrame(A, columns=providers, index=providers)
print(df)

# Create graph from shared matrix
G = nx.from_numpy_array(A)
print(G)

# Remove self-loop edges
G.remove_edges_from(nx.selfloop_edges(G))

# Plot size
plt.figure(figsize=(8.3, 5))
plt.margins(0.15)
# Draw graph
pos = nx.circular_layout(G)  # positions for all nodes - seed for reproducibility
# nodes
nx.draw_networkx_nodes(G, pos, node_color=clusters, cmap=plt.cm.Set2)
# edges
# color edges when numbers shared > 0
edges = [(u, v, d) for (u, v, d) in G.edges(data=True) if d["weight"] > 0]
nx.draw_networkx_edges(G, pos, edgelist=edges, alpha=0.4)
# labels for nodes
node_labels = {i: f'{providers[i]}\n{A[i,i]:.0f}\nCluster #{clusters[i]}' for i, v in enumerate(providers)}
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=8)
# labels for edges
edge_labels = {(u, v): "{0:.0f}".format(d['weight']) for (u, v, d) in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.show()
import networkx as nx 
import matplotlib.pyplot as plt
import sys, random as rnd
from itertools import permutations

# Create a complete oriented graph containing a specific number of vertices with random values 
# for customers demand and profit and edges with random weights
def create_graph(num_v, draw = False):
    
    # Create empty graph
    G = nx.DiGraph()

    # Add vertex 0 as the depot
    G.add_node(0, demand = 0, profit = 0)

    # Add vertices with attributes for demand and profit of customer
    for i in range(1, num_v):
        G.add_node(i, demand = rnd.randint(1, 1000), profit = rnd.randint(1, 1000))

    # Add edges with an attribute for elapsed time between all permutations of vertices
    for e in permutations(G.nodes, 2):
        G.add_edge(e[0], e[1], weight = rnd.randint(1, 120))

    # Print graph information
    weight = nx.get_edge_attributes(G, 'weight')
    print("|V(G)| = {}\nV = \nDemand: {}\nProfit: {}\n".format(G.number_of_nodes(), nx.get_node_attributes(G, "demand"), nx.get_node_attributes(G, "profit")))
    print("|E(G)| = {}\nE = \n{}\n".format(G.number_of_edges(), nx.get_edge_attributes(G, 'weight')))

    if draw == True:
        # Show graph representation
        plt.figure(figsize = (12, 12)) 
        nx.draw_networkx(G, pos = nx.circular_layout(G), with_labels=True, node_color ='green')
        nx.draw_networkx_edge_labels(G,pos = nx.circular_layout(G), edge_labels=weight)
        plt.show()

    return G

# Verify user input
if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python graph.py <#vertices>")
    else:
        num_v = int(sys.argv[1])
        if 2 <= num_v:
            G = create_graph(num_v)
        else:
            sys.exit("Error: graph containing a single vertex does not make sense for the SDCTOP problem")
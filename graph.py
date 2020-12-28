import networkx as nx, matplotlib.pyplot as plt, sys, random as rnd
from itertools import permutations

# Create a complete oriented graph containing a specific number of vertices with random values 
# for customers demand and profit and edges with random weights
def create_graph(num_v, draw = False):
    
    # Create empty graph
    G = nx.DiGraph()
    total_profit, total_demand, total_weight = 0, 0, 0

    # Add vertex 0 as the depot
    G.add_node(0, demand = 0, profit = 0)

    # Add vertices with attributes for demand and profit of customer
    for i in range(1, num_v):
        profit = rnd.randint(1, 1000)
        demand = rnd.randint(1, 1000)
        G.add_node(i, profit = profit, demand = demand)
        total_profit += profit
        total_demand += demand

    # Add edges with an attribute for elapsed time (weight) between all permutations of vertices
    for e in permutations(G.nodes, 2):
        weight = rnd.randint(1, 60)
        G.add_edge(e[0], e[1], weight = weight)
        total_weight += weight

    G.graph["profit"] = total_profit
    G.graph["demand"] = total_demand
    G.graph["weight"] = total_weight

    # Show graph information
    graph_info(G, True)

    return G

# Print graph information
def graph_info(G, draw = False):

    weight = nx.get_edge_attributes(G, 'weight')
    print("|V(G)| = {}\nV = \nProfit: {}\nDemand: {}\n".format(G.number_of_nodes(), nx.get_node_attributes(G, "profit"), nx.get_node_attributes(G, "demand")))
    print("|E(G)| = {}\nE = \n{}\n".format(G.number_of_edges(), nx.get_edge_attributes(G, 'weight')))
    print("Total profit = {}".format(G.graph["profit"]))
    print("Total demand = {}".format(G.graph["demand"]))
    print("Total weight = {}\n".format(G.graph["weight"]))

    if draw == True:
        # Show graph representation
        draw_graph(G)

# Draw graph representation
def draw_graph(G):
    weight = nx.get_edge_attributes(G, 'weight')
    fig = plt.figure(figsize = (12, 12))
    nx.draw_networkx(G, pos = nx.circular_layout(G), with_labels=True, node_color ='green')
    nx.draw_networkx_edge_labels(G,pos = nx.circular_layout(G), edge_labels=weight)
    fig.canvas.set_window_title("Graph")
    plt.show()

# Return a list of all cycles in graph G, with an optional root vertex
def find_all_cycles(G, root = None):
    C = nx.simple_cycles(G)
    cycles_list = []

    if root == None:
        #print("All cycles in G:\n")
        for cycle in C:
            #print(cycle)
            cycles_list.append(cycle)
    else:
        #print("All cycles in G with root {}\n:".format(root))
        for cycle in C:
            if root in cycle:
                #print(cycle)
                cycles_list.append(cycle)

    cycles_list.sort(key = len)
    #print(cycles_list)
    return cycles_list

# Return a dictionary containing the attributes profit, demand and weight of a cycle
def get_cycle_attr(G, cycle):
    profit, demand, weight = 0, 0, 0
    #root = cycle[0]
    cycle_attr = {}

    for customer in range (0, len(cycle), 1):
        profit += G.nodes.get(cycle[customer]).get("profit")
        demand += G.nodes.get(cycle[customer]).get("demand")

        if customer < (len(cycle) - 1):
            weight += G.edges.get((cycle[customer], cycle[customer + 1])).get("weight")
        else:
            weight += G.edges.get((cycle[len(cycle) - 1], cycle[0])).get("weight")
    
    cycle_attr = {"profit" : profit, "demand" : demand, "weight" : weight}
    #print("The cycle \n{}\n has attributes:\n{}\n".format(cycle, cycle_attr))
    return cycle_attr

# Return a nested dictionary where cycles are keys and their attributes profit, demand and weigth are values. A root vertex for the cycles is optional.
def get_all_cycles_attr(G, root = None):
    cycles_list = find_all_cycles(G, 0)

    all_cycles_attr = {}
    for cycle in cycles_list:
        all_cycles_attr[tuple(cycle)] = get_cycle_attr(G, cycle)

    print("All cycles and their attributes:\n{}\n".format(all_cycles_attr))
    return all_cycles_attr

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
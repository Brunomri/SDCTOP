import networkx as nx, matplotlib.pyplot as plt, sys, random as rnd
from itertools import permutations

# Functions to manage graph instances

# Create a complete oriented graph containing a specific number of vertices with random values 
# for customers demand and profit and edges with random weights
def create_graph(num_v, draw = False, save_graph = False):
    
    # Create empty directed graph
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

    # Graph attributes are the sum of the corresponding
    # attributes for each edge and vertex
    G.graph["profit"] = total_profit
    G.graph["demand"] = total_demand
    G.graph["weight"] = total_weight

    # Show graph information
    if draw == True:
        graph_info(G, save_graph, True)
    else:
        graph_info(G, save_graph, False)

    return G

# Create cycles in graph G based on a cycles attributes dictionary
def create_cycles(G, all_cycles_attr, draw = False):
    cycles = []

    # Create one cycle for each entry in the dictionary
    for cycle in all_cycles_attr:
        # Create empty directed graph
        C = nx.DiGraph()

        # Add vertices from the cycle dictionary keys and get their profit and
        # demand attributes from original graph G
        for v in cycle:
            profit = G.nodes.get(v).get("profit")
            demand = G.nodes.get(v).get("demand")
            C.add_node(v, profit = profit, demand = demand)

        # Add edges from the cycle dictionary keys and get their weight 
        # from original graph G
        nodes = list(C.nodes.keys())
        for v in range (len(nodes) - 1):
            v1 = nodes[v]
            v2 = nodes[v + 1]
            e = (v1, v2)
            weight = G.edges.get(e).get("weight")
            C.add_edge(v1, v2, weight = weight)

        # Add edge connecting the first and last vertices from the cycle
        e = (nodes[len(nodes) - 1], nodes[0])
        weight = G.edges.get(e).get("weight")
        C.add_edge(e[0], e[1], weight = weight)

        # Cycle attributes are the sum of the corresponding
        # attributes for each edge and vertex
        C.graph["profit"] = all_cycles_attr[cycle]["profit"]
        C.graph["demand"] = all_cycles_attr[cycle]["demand"]
        C.graph["weight"] = all_cycles_attr[cycle]["weight"]

        if draw == True:
            graph_info(C, True)
        else:
            graph_info(C, False)

        cycles.append(C)

    return cycles

# Print graph information
def graph_info(G, save_graph, draw = False):

    weight = nx.get_edge_attributes(G, 'weight')
    print("-------------------------------------------")
    print("|V(G)| = {}\nV = \nProfit: {}\nDemand: {}\n".format(G.number_of_nodes(), nx.get_node_attributes(G, "profit"), nx.get_node_attributes(G, "demand")))
    print("|E(G)| = {}\nE = \n{}\n".format(G.number_of_edges(), nx.get_edge_attributes(G, 'weight')))
    print("Total profit = {}".format(G.graph["profit"]))
    print("Total demand = {}".format(G.graph["demand"]))
    print("Total weight = {}".format(G.graph["weight"]))
    print("-------------------------------------------\n")

    draw_graph(G, save_graph, draw)

# Draw graph representation
def draw_graph(G, save_graph, draw):
    weight = nx.get_edge_attributes(G, 'weight')
    fig = plt.figure(figsize = (12, 12))
    nx.draw_networkx(G, pos = nx.circular_layout(G), with_labels=True, node_color ='green')
    nx.draw_networkx_edge_labels(G,pos = nx.circular_layout(G), edge_labels=weight)
    if save_graph:
        nx.write_gpickle(G, 'graph.gpl')
    fig.canvas.set_window_title("Graph")
    if draw:
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
            print("#Cycles = {}".format(len(cycles_list)), end = "\r")
    else:
        #print("All cycles in G with root {}\n:".format(root))
        for cycle in C:
            if root in cycle:
                #print(cycle)
                cycles_list.append(cycle)
                print("#Cycles = {}".format(len(cycles_list)), end = "\r")

    cycles_list.sort(key = len)
    print("#Cycles = {}".format(len(cycles_list)))
    return cycles_list

# Return a dictionary containing the attributes profit, demand and weight of a cycle
def get_cycle_attr(G, cycle):
    profit, demand, weight = 0, 0, 0
    cycle_attr = {}

    for customer in range (0, len(cycle), 1):
        profit += G.nodes.get(cycle[customer]).get("profit")
        demand += G.nodes.get(cycle[customer]).get("demand")

        if customer < (len(cycle) - 1):
            weight += G.edges.get((cycle[customer], cycle[customer + 1])).get("weight")
        else:
            weight += G.edges.get((cycle[len(cycle) - 1], cycle[0])).get("weight")
    
    cycle_attr = {"profit" : profit, "demand" : demand, "weight" : weight}
    return cycle_attr

# Return a nested dictionary where cycles are keys and their attributes profit, demand and weigth are values. A root vertex for the cycles is optional.
def get_all_cycles_attr(G, root = None):
    print("Finding all cycles\n")
    cycles_list = find_all_cycles(G, 0)

    all_cycles_attr = {}
    for cycle in cycles_list:
        all_cycles_attr[tuple(cycle)] = get_cycle_attr(G, cycle)

    #print("All cycles and their attributes:\n{}\n".format(all_cycles_attr))
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
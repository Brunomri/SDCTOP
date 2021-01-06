import sys, graph as g, solver as s, networkx as nx

# Driver program
if len(sys.argv) != 6 or (sys.argv[1] != '-c' and sys.argv[1] != '-g'):
    sys.exit("Usage: python sdctop.py -c <#customers> <vehicle_capacity> <#vehicles> <route_time_limit> OR python sdctop.py -g <gpl_graph_path> <vehicle_capacity> <#vehicles> <route_time_limit>")
else:
    if sys.argv[1] == "-c":
        num_customers = int(sys.argv[2])
    else:
        graph_path = str(sys.argv[2])
        G = nx.read_gpickle(graph_path)
        num_customers = len(G)
    v_capacity = int(sys.argv[3])
    num_vehicles = int(sys.argv[4])
    time_lim = int(sys.argv[5])

    if sys.argv[1] == "-g":
        print("Graph path: {}".format(graph_path))
        print("Number of customers: {}".format(num_customers-1))
        print("Total graph profit = {}".format(G.graph["profit"]))
        print("Total graph demand = {}".format(G.graph["demand"]))
        print("Total graph weight = {}".format(G.graph["weight"]))
    else:
        print("Number of customers: {}".format(num_customers))
    print("Vehicle capacity: {}".format(v_capacity))
    print("Number of vehicles: {}".format(num_vehicles))
    print("Route time limit: {}\n".format(time_lim))

    if num_customers >= 2 and v_capacity >= 1 and num_vehicles >= 1 and time_lim >= 1:
        if sys.argv[1] == "-c":
            G = g.create_graph(num_customers + 1, True, True)
            all_routes = g.get_all_cycles_attr(G, 0)
            s.solve(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim, 10)
        else:
            g.draw_graph(G, False, True)
            all_routes = g.get_all_cycles_attr(G, 0)
            s.solve(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim, 10, graph_path)
    else:
        sys.exit("Error: #customer needs to be >= 2, vehicle capacity >= 1, #vehicles >= 1, route time limit >= 1")
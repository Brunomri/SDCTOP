import sys, graph as g, solver as s

# Driver program
if len(sys.argv) != 5:
    sys.exit("Usage: python sdctop.py <#customers> <vehicle_capacity> <#vehicles> <route_time_limit>")
else:
    num_customers = int(sys.argv[1])
    v_capacity = int(sys.argv[2])
    num_vehicles = int(sys.argv[3])
    time_lim = int(sys.argv[4])

    print("Number of customers: {}".format(num_customers))
    print("Vehicle capacity: {}".format(v_capacity))
    print("Number of vehicles: {}".format(num_vehicles))
    print("Route time limit: {}\n".format(time_lim))

    if num_customers >= 2 and v_capacity >= 1 and num_vehicles >= 1 and time_lim >= 1:
        G = g.create_graph(num_customers + 1)
        all_routes = g.get_all_cycles_attr(G, 0)
        solution = s.solve(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim, 10)
    else:
        sys.exit("Error: #customer needs to be >= 2, vehicle capacity >= 1, #vehicles >= 1, route time limit >= 1")
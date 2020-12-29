import graph as g

# Solve an instance of the SDCTOP problem

# Generate a feasible initial solution build upon all the existing routes in the network
def initial_sol(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim):
    total_time, total_profit, total_delivered, num_routes = 0, 0, 0, 0
    selected_routes = {}
    solution = {}
    iter = 0

    # Examine every route while the number of routes in the soluiton is 
    # less than the number of vehicles
    visited = []

    for route in all_routes:
        if num_routes < num_vehicles and len(visited) < num_customers:
            route_profit = all_routes.get(route)["profit"]
            route_time = all_routes.get(route)["weight"]
            route_delivered = all_routes.get(route)["demand"]

            # Check route feasibility, to add a route to the solution, time must be 
            # less than the maximum time limit and the delivered quantity must not exceed the vehicle capacity
            if route_time <= time_lim and route_delivered <= v_capacity:
                # Check the intersection of visited customers and the current route customers to avoid
                # visiting the same customer twice
                if len(set(visited).intersection(set(route))) == 0:
                    selected_routes[route] = all_routes[route]
                    visited.extend(route[1:])
                    num_routes += 1
                    total_time += route_time
                    total_profit += route_profit
                    total_delivered += route_delivered
        else:
            break

    g.create_cycles(G, selected_routes, True)
    # Solution is a dictionary where the key is a tuple of tuples containing routes and the value is a dictionary of
    # route attributes which are profit, time and demand
    solution[tuple(selected_routes.keys())] = {"profit" : total_profit, "time" : total_time, "demand" : total_delivered}
    #print("Initial solution:\n{}\n".format(selected_routes))
    print("Initial solution:\n{}\n".format(solution))
    return solution

def solve(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim):
    init_s = initial_sol(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim)
    return init_s
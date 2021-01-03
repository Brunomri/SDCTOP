import graph as g, copy

# Solve an instance of the SDCTOP problem

# Generate a feasible initial solution build upon all the existing routes in the network.
# This initial solution is a CTOP solution, it won't consider split deliveries.
def initial_sol(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim):
    total_time, total_profit, total_delivered, num_routes = 0, 0, 0, 0
    selected_routes = {}
    solution = {}
    visited = 0

    # Find a route for each available vehicle unless all the
    # customers have been already visited 
    for v in range (num_vehicles):
        if visited >= num_customers:
            break
        else:
            # Keep track of the feasible route with maximum profit
            best_route = ()
            max_profit = 0

            # Examine all existing routes
            if len(all_routes) > 0:
                for route in all_routes.copy():
                    route_time = all_routes.get(route)["weight"]
                    route_delivered = all_routes.get(route)["demand"]
                    # Check route feasibility, to add a route to the solution, time must be 
                    # less than the maximum time limit and the delivered quantity must not exceed the vehicle capacity
                    if route_time <= time_lim and route_delivered <= v_capacity:
                        route_profit = all_routes.get(route)["profit"]
                        # If the current route is feasible and its profit is larger
                        # than the previous maximum profit, this route is set as the best route
                        # and its profit is the new maximum profit
                        if route_profit > max_profit:
                            best_route = route
                            max_profit = route_profit
                        # If the current route has the same profit as the best route, it will
                        # replace the best route if its time is smaller than the best route time
                        elif route_profit == max_profit:
                            if route_time < all_routes[best_route]["weight"]:
                                best_route = route
                    # Delete infeasible routes
                    else:
                        all_routes.pop(route)

                # Add best route as the selected route for the current vehicle
                # and get its attributes for further use in the solution
                selected_routes[best_route] = all_routes[best_route]
                total_time += selected_routes[best_route]["weight"]
                total_profit += selected_routes[best_route]["profit"]
                total_delivered += selected_routes[best_route]["demand"]
                visited = len(best_route) - 1

                # Ensure that each customer is served by one
                # vehicle at most (CTOP constraint)
                for customer in best_route[1:]:
                    for route in all_routes.copy():
                        if customer in route:
                            all_routes.pop(route)

    # Display selected routes and build initial solution
    g.create_cycles(G, selected_routes, True)
    solution[tuple(selected_routes.keys())] = {"profit" : total_profit, "time" : total_time, "demand" : total_delivered}
    print("Initial solution:\n{}\n".format(solution))
    return solution, selected_routes

# Find the neighbourhood of a given solution. The neighborhood is built upon the selected
# routes by adding or removing one single customer.
def find_neighborhood(G, all_routes, selected_routes):
    neighborhood = {}

    # Iterate over the selected routes to find their neighbors by 
    # adding or removing one single customer
    for route in selected_routes:
        unvisited = set(route).symmetric_difference(G.nodes)

        # If the route doesn't visit all the customers, a new unvisited
        # customer can be added
        if len(route) < len(G.nodes):
            for customer in unvisited:
                l_route = list(route)
                l_route.append(customer)
                new_route = tuple(l_route)
                if new_route not in neighborhood:
                    neighborhood[new_route] = all_routes[new_route]

        # If the route visits at least 2 customers, one visited
        # customer can be removed
        if len(route) > 2:
            for customer in route[1:]:
                l_route = list(route)
                l_route.remove(customer)
                new_route = tuple(l_route)
                if new_route not in neighborhood:
                    neighborhood[new_route] = all_routes[new_route]

    return neighborhood

def solve(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim):
    all_routes2 = copy.deepcopy(all_routes)
    init_s, selected_routes = initial_sol(G, all_routes2, num_customers, v_capacity, num_vehicles, time_lim)
    neighborhood = find_neighborhood(G, all_routes, selected_routes)
    return init_s
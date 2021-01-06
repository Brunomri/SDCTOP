import graph as g, copy, math, sys, time, csv

# Solve an instance of the SDCTOP problem

# Generate a feasible initial solution build upon all the existing routes in the network.
# This initial solution is a CTOP solution, it won't consider split deliveries.
def initial_sol(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim):
    total_time, total_profit, total_delivered, num_routes = 0, 0, 0, 0
    selected_routes = {}
    solution = {}
    visited = 0
    print("Finding an initial solution\n")

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
                if len(all_routes) == 0:
                    sys.exit("There are no routes to satisfy the imposed vehicle capacity and time limit contraints.\n")

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
    solution[tuple(selected_routes.keys())] = {"profit" : total_profit, "demand" : total_delivered, "weight" : total_time}
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

# Run the tabu search starting from a CTOP initial solution and build a best solution for SDCTOP
def tabu_search(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim, init_s, tenure):
    # Best solution and best candidate solution start with the initial solution
    best_sol = init_s
    best_candidate = init_s
    # The tabu list starts with the routes of the initial solution
    tabu_list = []
    tabu_list.append(init_s.keys())
    # non_improving keeps track of the number of iterations without profit growth
    non_improving = 0

    print("Starting Tabu Search procedure\n")

    # The stopping condition is 20 iterations without improving the profit of the solution
    while(non_improving <= 20):
        # Find the neighborhood of the current best candidate for the solution
        neighborhood = find_neighborhood(G, all_routes, best_candidate)
        neighbor_routes = neighborhood.keys()
        total_profit, total_time, total_demand = 0, 0, 0
        # served is a list to track the customers whose demand was already fulfilled
        served = []
        # new_candidate is dictionary to store a new candidate for the best solution
        new_candidate = {}
        # split_delivery keeps track of customers who received split deliveries and will need to be
        # visited again in order to fulfill their demand completely
        split_delivery = {}

        # Iterate over the routes in the neighborhood of the current best solution
        for candidate_route in neighbor_routes:
            # The route is ignored if it contains already served customers
            if len(set(candidate_route).intersection(served)) > 0:
                continue

            # The route is considered if it is not in the tabu list or if it meets the aspiration criterion, which is to contain
            # a customer who previously received a split delivery
            if candidate_route not in tabu_list or len(set(candidate_route).intersection(split_delivery)) > 0:
                if len(split_delivery) > 0:
                    for customer in split_delivery.keys():
                        if customer not in candidate_route:
                            continue
                
                candidate_time = all_routes[candidate_route]["weight"]
                # If the current candidate solution has not exceeded the number of vehicles
                # the current candidate route does not exceed the time limit, more routes might be included
                if len(new_candidate) < num_vehicles and candidate_time <= time_lim:
                    candidate_demand = all_routes[candidate_route]["demand"]
                    # If the demand of the current candidate route is less than the vehicle capacity, all customers
                    # will have their demand fulfilled, no split deliveries are required and this route is added to the
                    # current candidate solution
                    if candidate_demand <= v_capacity:
                        candidate_profit = all_routes[candidate_route]["profit"]

                        # In this case the route is added to the solution with all the original attributes
                        # from the all_routes dictionary
                        new_candidate[candidate_route] = all_routes[candidate_route]
                        total_profit += candidate_profit
                        total_time += candidate_time
                        total_demand += candidate_demand
                        #tabu_list.append(candidate)

                        # Served customers will be appended to the served list. If the route serves a customers who 
                        # was previosly in the split deliveries list, he will be removed from the list 
                        # as his demand is now fulfilled
                        for customer in candidate_route[1:]:
                            served.append(customer)
                            if customer in split_delivery.keys():
                                split_delivery.pop(customer)

                    # If the route exceeds the vehicle capacity, split deliveries will be necessary         
                    else:
                        # The number of vehicles required to serve the route must be less than
                        # the number of vehicles still available for delivery in this candidate solution.
                        # Otherwise, this candidate is ignored
                        req_vehicles = math.ceil(candidate_demand / v_capacity)
                        remaining_routes = num_vehicles - len(new_candidate)
                        if remaining_routes >= req_vehicles:
                            #new_candidate[candidate_route] = all_routes[candidate_route]
                            total_time += candidate_time
                            available_demand = v_capacity
                            candidate_profit, candidate_demand = 0, 0

                            # Iterate over the customers in the route to discover which ones can receive their
                            # whole demand and whiich ones will receive split deliveries
                            for customer in candidate_route[1:]:
                                customer_profit = G.nodes.get(customer).get("profit")

                                # If the customer was already part of a split delivery, his demand
                                # is updated with the remaining demand stored in the split delivery dictionary
                                if customer in split_delivery:
                                    customer_demand = split_delivery[customer]
                                # Otherwise his demand is the demand value from its vertex from the original
                                # graph instance
                                else:
                                    customer_demand = G.nodes.get(customer).get("demand")

                                # If the vehicle still has capacity to serve this customer, his profit
                                # is added to the candidate route profit, his demand
                                # is added to the candidate route demand and subtracted from
                                # the available demand and the customer is appended to the served list
                                if available_demand >= customer_demand:
                                    candidate_profit += customer_profit
                                    available_demand -= customer_demand
                                    served.append(customer)
                                    # If the customer was part of the split deliveries, he will be
                                    # removed from it
                                    if customer in split_delivery:
                                        split_delivery.pop(customer)

                                    candidate_demand += customer_demand
                                # Otherwise, the candidate route demand is increased by the available demand which
                                # was delivered to this customer (after visiting all the customers it should be equal to vehicle capacity).
                                # The customer and his remaining demand form a key-value pair that is added to the split delivery dictionary and
                                # the available demand is updated to 0
                                else:
                                    candidate_demand += available_demand
                                    split_delivery[customer] = customer_demand - available_demand
                                    available_demand = 0

                            # After all customers are examined, the candidate route is added to the candidate solution
                            new_candidate[candidate_route] = {"profit" : candidate_profit, "weight" : candidate_time, "demand" : candidate_demand}

                            total_profit += candidate_profit
                            total_demand += candidate_demand
                        else:
                            continue
            else:
                continue
            #print("Current candidate solution:\n{}\n".format(new_candidate))
        # If the new candidade solution contains at least one feasible route, it will be
        # considered the best candidate solution
        if len(new_candidate) > 0:
            best_candidate = new_candidate

        #print("Best candidate solution:\n{}\n".format(best_candidate))
        # Update the tabu list appending the routes in the best candidate solution
        # and removing the oldest entry if list size exceeds the tabu tenure parameter
        for route in best_candidate:
            if route not in tabu_list:
                if(len(tabu_list) > tenure):
                    tabu_list.pop(0)
                tabu_list.append(route)

        # If split deliveries still exist after all the routes in the neighborhood were
        # examined, it means that at least one customer had his demand partially delivered.
        # Therefore the solution is infeasible, the best solution remains unchanged and this iteration
        # is considered non-improving
        if len(split_delivery) > 0:
            non_improving += 1
            continue
        # Otherwise, the profit of the current candidate solution is compared to the profit
        # of the best solution found so far. If the candidate solution has a higher profit, it
        # becomes the best solution, if not, the iteration is considered non-improving
        else:
            best_profit = 0
            for route in best_sol:
                best_profit += all_routes[route]["profit"]
            if total_profit >= best_profit:
                best_sol = best_candidate
                #print("Remaining demand of customers served by split deliveries: \n{}\n".format(split_delivery))
                #print("Best solution:\n{}\n".format(best_sol))
                if total_profit == best_profit:
                    non_improving += 1
            else:
                non_improving += 1
    
    print("Best solution selected routes:\n{}\n".format(best_sol))
    # After meeting the stop criterion, return the best solution
    return best_sol

def best_solution_info(G, v_capacity, num_vehicles, time_lim, tenure, init_sol, best_sol, runtime, instance):
    best_sol_profit, best_sol_weight, best_sol_demand = 0, 0, 0
    best_sol_info = {}

    graph_profit = G.graph["profit"]
    graph_demand = G.graph["demand"]
    graph_weight = G.graph["weight"]

    for route in best_sol:
        best_sol_profit += best_sol[route]["profit"]
        best_sol_weight += best_sol[route]["weight"]
        best_sol_demand += best_sol[route]["demand"]

    print("Procedure completed, showing results:\n")
    num_customers = len(G.nodes) - 1
    print("Number of customers = {}\n".format(num_customers))
    best_sol_info[tuple(best_sol.keys())] = {"profit" : best_sol_profit, "demand" : best_sol_demand, "weight" : best_sol_weight}
    print("Initial solution:\n{}\nBest solution:\n{}\nRuntime(s) = {}\n".format(init_sol, best_sol_info, runtime))

    init_sol_attr = list(init_sol.values())[0]
    init_sol_profit = init_sol_attr["profit"]
    init_sol_weight = init_sol_attr["weight"]
    init_sol_demand = init_sol_attr["demand"]

    init_profit_percent = (init_sol_profit / graph_profit) * 100
    init_demand_percent = (init_sol_demand / graph_demand) * 100
    init_weight_percent = (init_sol_weight / graph_weight) * 100

    print("Initial and best solution performance compared (% of the network):\n")
    print("Initial profit collected = {}%".format(init_profit_percent))
    print("Initial demand served = {}%".format(init_demand_percent))
    print("Initial time spent = {}%\n".format(init_weight_percent))

    best_profit_percent = (best_sol_profit / graph_profit) * 100
    best_demand_percent = (best_sol_demand / graph_demand) * 100
    best_weight_percent = (best_sol_weight / graph_weight) * 100

    print("Best profit collected = {}%".format(best_profit_percent))
    print("Best demand served = {}%".format(best_demand_percent))
    print("Best time spent = {}%\n".format(best_weight_percent))

    profit_improve = ((best_sol_profit / init_sol_profit) - 1) * 100
    print("Profit improvement from initial to best solution = {}%".format(profit_improve))

    with open("results.csv", "a", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow(["Instance", "#Customers", "Capacity", "#Vehicles", "Time Limit", "Solution", "Runtime(s)", "Tenure", "Routes", "Solution profit", "Solution demand", "Solution time", "Profit(%)", "Demand(%)", "Time(%)", "Profit improvement(%)"])
        writer.writerow([instance, num_customers, v_capacity, num_vehicles, time_lim, "Initial", "", "", list(init_sol.keys()), init_sol_profit, init_sol_demand, init_sol_weight, init_profit_percent, init_demand_percent, init_weight_percent, ""])
        writer.writerow([instance, num_customers, v_capacity, num_vehicles, time_lim, "Best", runtime, tenure, list(best_sol.keys()), best_sol_profit, best_sol_demand, best_sol_weight, best_profit_percent, best_demand_percent, best_weight_percent, profit_improve])
        writer.writerow("")
        file.close()

def solve(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim, tenure, instance = "random"):
    start = time.time()
    all_routes2 = copy.deepcopy(all_routes)
    init_s, selected_routes = initial_sol(G, all_routes2, num_customers, v_capacity, num_vehicles, time_lim)
    best_sol = tabu_search(G, all_routes, num_customers, v_capacity, num_vehicles, time_lim, selected_routes, tenure)
    end = time.time()
    runtime = end - start
    best_solution_info(G, v_capacity, num_vehicles, time_lim, tenure, init_s, best_sol, runtime, instance)
    print("Show details from the initial solution:")
    g.create_cycles(G, selected_routes, True, "Initial Solution")
    print("Show details from the best solution:")
    g.create_cycles(G, best_sol, True, "Best Solution")
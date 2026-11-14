from gurobipy import Model, GRB, quicksum
import matplotlib.pyplot as plt
import networkx as nx

# Function to get input from the user
def get_user_input():
    print("Generalized Facility Location Problem Solver")
    
    # Number of facilities and customers
    num_facilities = int(input("Enter the number of facilities: "))
    num_customers = int(input("Enter the number of customers: "))
    
    # Fixed costs for facilities
    fixed_costs = []
    print("Enter the fixed costs for each facility:")
    for i in range(num_facilities):
        cost = float(input(f"  Fixed cost for facility {i+1}: "))
        fixed_costs.append(cost)
    
    # Transportation costs
    transportation_costs = []
    print("Enter the transportation costs (rows: facilities, columns: customers):")
    for i in range(num_facilities):
        row = list(map(float, input(f"  Costs for facility {i+1} (space-separated): ").split()))
        transportation_costs.append(row)
    
    # Facility capacities
    capacities = []
    print("Enter the capacity for each facility (compulsory):")
    for i in range(num_facilities):
        cap = float(input(f"  Capacity for facility {i+1}: "))
        capacities.append(cap)
    
    # Customer demands
    demands = []
    print("Enter the demand for each customer:")
    for j in range(num_customers):
        demand = float(input(f"  Demand for customer {j+1}: "))
        demands.append(demand)
    
    # Option to display graph
    display_graph = input("Do you want to display the graph? (yes/no): ").lower() == 'yes'
    
    return num_facilities, num_customers, fixed_costs, transportation_costs, capacities, demands, display_graph

# Generalized FLP solver with fixed capacities
def solve_flp(num_facilities, num_customers, fixed_costs, transportation_costs, capacities, demands):
    # Create the model
    model = Model("Generalized_Facility_Location")
    
    # Decision variables
    y = model.addVars(num_facilities, vtype=GRB.BINARY, name="Open")  # Facility open/close variables
    x = model.addVars(num_facilities, num_customers, vtype=GRB.BINARY, name="Assign")  # Assignment variables

    # Objective function: Minimize fixed costs + transportation costs
    model.setObjective(
        quicksum(fixed_costs[i] * y[i] for i in range(num_facilities)) +
        quicksum(transportation_costs[i][j] * x[i, j] for i in range(num_facilities) for j in range(num_customers)),
        GRB.MINIMIZE
    )

    # Constraints
    # Each customer must be assigned to exactly one facility
    for j in range(num_customers):
        model.addConstr(quicksum(x[i, j] for i in range(num_facilities)) == 1, name=f"Customer_Assign_{j}")

    # A facility must be open if it serves any customers
    for i in range(num_facilities):
        for j in range(num_customers):
            model.addConstr(x[i, j] <= y[i], name=f"Facility_Open_{i}_Customer_{j}")

    # Capacity constraints: Total demand served by a facility must not exceed its capacity
    for i in range(num_facilities):
        model.addConstr(
            quicksum(demands[j] * x[i, j] for j in range(num_customers)) <= capacities[i],
            name=f"Capacity_{i}"
        )

    # Solve the model
    model.optimize()

    # Display results
    if model.status == GRB.OPTIMAL:
        print("\nOptimal Solution:")
        print("Facilities Opened:")
        for i in range(num_facilities):
            if y[i].x > 0.5:
                print(f"  Facility {i+1} is open.")
        
        print("\nCustomer Assignments:")
        for i in range(num_facilities):
            for j in range(num_customers):
                if x[i, j].x > 0.5:
                    print(f"  Customer {j+1} is served by Facility {i+1}.")
        
        print("\nFacility Capacities Used:")
        for i in range(num_facilities):
            capacity_used = sum(demands[j] * x[i, j].x for j in range(num_customers))
            if y[i].x > 0.5:
                print(f"  Facility {i+1}: {capacity_used}/{capacities[i]}")
    else:
        print("No optimal solution found.")

    return y, x, model

# Graph visualization function
def visualize_graph(num_facilities, num_customers, fixed_costs, transportation_costs, capacities, demands, y, x, display_graph):
    if not display_graph:
        return
    
    # Create the graph
    G = nx.Graph()
    
    # Add facilities (squares) and customers (circles)
    for i in range(num_facilities):
        if y[i].x > 0.5:  # Only add open facilities
            G.add_node(f"F{i+1}", pos=(i, 0), color='blue', shape='s', size=1000)  # Square for facilities
    for j in range(num_customers):
        G.add_node(f"C{j+1}", pos=(j, 1), color='red', shape='o', size=500)  # Circle for customers
    
    # Add edges between facilities and customers based on assignments
    for i in range(num_facilities):
        for j in range(num_customers):
            if x[i, j].x > 0.5:  # If customer j is assigned to facility i
                demand = demands[j]
                transportation_cost = transportation_costs[i][j]
                weight = transportation_cost * demand  # Edge weight based on demand and transportation cost
                G.add_edge(f"F{i+1}", f"C{j+1}", weight=weight)
    
    # Plot the graph
    pos = nx.get_node_attributes(G, 'pos')
    colors = [node[1]['color'] for node in G.nodes(data=True)]
    shapes = [node[1]['shape'] for node in G.nodes(data=True)]
    sizes = [node[1]['size'] for node in G.nodes(data=True)]
    
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=sizes, font_size=12)
    
    # Draw edge labels (weights)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    plt.show()

# Main function
if __name__ == "__main__":
    # Get inputs from the user
    num_facilities, num_customers, fixed_costs, transportation_costs, capacities, demands, display_graph = get_user_input()

    # Solve the problem
    y, x, model = solve_flp(num_facilities, num_customers, fixed_costs, transportation_costs, capacities, demands)

    # Optionally visualize the graph
    visualize_graph(num_facilities, num_customers, fixed_costs, transportation_costs, capacities, demands, y, x, display_graph)

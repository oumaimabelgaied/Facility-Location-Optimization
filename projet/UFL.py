from gurobipy import Model, GRB, quicksum
import matplotlib.pyplot as plt
import networkx as nx
import random

# Function to get input from the user
def get_user_input():
    print("Uncapacitated Facility Location Problem Solver")
    
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

    return num_facilities, num_customers, fixed_costs, transportation_costs

# Function to solve the FLP
def solve_flp(num_facilities, num_customers, fixed_costs, transportation_costs, visualize_graph=False):
    # Create the optimization model
    model = Model("Uncapacitated_Facility_Location")
    
    # Decision variables
    x = model.addVars(num_facilities, vtype=GRB.BINARY, name="Open")  # Facility open/close variables
    y = model.addVars(num_facilities, num_customers, vtype=GRB.BINARY, name="Assign")  # Assignment variables

    # Objective function: Minimize fixed costs + transportation costs
    model.setObjective(
        quicksum(fixed_costs[i] * x[i] for i in range(num_facilities)) +
        quicksum(transportation_costs[i][j] * y[i, j] for i in range(num_facilities) for j in range(num_customers)),
        GRB.MINIMIZE
    )

    # Constraints
    # Each customer must be assigned to exactly one facility
    for j in range(num_customers):
        model.addConstr(quicksum(y[i, j] for i in range(num_facilities)) == 1, name=f"Customer_Assign_{j}")

    # A facility must be open if it serves any customers
    for i in range(num_facilities):
        for j in range(num_customers):
            model.addConstr(y[i, j] <= x[i], name=f"Facility_Open_{i}_Customer_{j}")

    # Solve the model
    model.optimize()

    # Display results
    facility_colors = {}  # To store facility colors for graph visualization
    if model.status == GRB.OPTIMAL:
        print("\nOptimal Solution:")
        print("Facilities Opened:")
        for i in range(num_facilities):
            if x[i].x > 0.5:
                print(f"  Facility {i+1} is open.")
                facility_colors[i] = (random.random(), random.random(), random.random())  # Assign a random color
        
        print("\nCustomer Assignments:")
        customer_assignments = {}  # To store customer-facility assignments for visualization
        for i in range(num_facilities):
            for j in range(num_customers):
                if y[i, j].x > 0.5:
                    print(f"  Customer {j+1} is served by Facility {i+1}.")
                    customer_assignments[j] = i

        # Visualize the graph if the user chooses to
        if visualize_graph:
            draw_facility_location_graph(
                num_facilities, num_customers, transportation_costs, facility_colors, customer_assignments
            )
    else:
        print("No optimal solution found.")

# Function to visualize the facility location graph
def draw_facility_location_graph(num_facilities, num_customers, transportation_costs, facility_colors, customer_assignments):
    # Create a graph using NetworkX
    G = nx.DiGraph()  # Directed graph to represent facility-to-customer connections
    
    # Add nodes for facilities and customers
    for i in range(num_facilities):
        G.add_node(f"F{i+1}", pos=(0, i), type="facility", color=facility_colors.get(i, "gray"))
    
    for j in range(num_customers):
        G.add_node(
            f"C{j+1}", pos=(1, j), type="customer", color=facility_colors.get(customer_assignments.get(j), "gray")
        )

    # Add edges with transportation costs as weights
    for i in range(num_facilities):
        for j in range(num_customers):
            G.add_edge(f"F{i+1}", f"C{j+1}", weight=transportation_costs[i][j])

    # Get node positions, types, and colors for plotting
    pos = nx.get_node_attributes(G, "pos")
    colors = [data["color"] for _, data in G.nodes(data=True)]

    # Draw the graph
    plt.figure(figsize=(10, 6))
    
    nx.draw(
        G, pos, 
        with_labels=True, 
        node_size=[800 if data["type"] == "facility" else 600 for _, data in G.nodes(data=True)],
        node_color=colors,
        edge_color="gray",
        font_weight="bold"
    )
    
    # Draw edge labels (transportation costs)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Add title and legend
    plt.title("Facility Location Graph")
    plt.legend(
        handles=[
            plt.Line2D([0], [0], marker="o", color="w", label="Facilities", markersize=10, markerfacecolor="lightblue"),
            plt.Line2D([0], [0], marker="s", color="w", label="Customers", markersize=10, markerfacecolor="orange")
        ],
        loc="upper left"
    )

    plt.show()

# Main function
if __name__ == "__main__":
    # Get inputs from the user
    num_facilities, num_customers, fixed_costs, transportation_costs = get_user_input()

    # Ask the user if they want to visualize the graph
    visualize_graph = input("Do you want to visualize the graph? (yes/no): ").strip().lower() == "yes"

    # Solve the problem and optionally visualize the graph
    solve_flp(num_facilities, num_customers, fixed_costs, transportation_costs, visualize_graph)

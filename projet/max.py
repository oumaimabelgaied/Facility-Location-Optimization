import gurobipy as grb

def max_covering_with_distance(num_installations, num_demands, distances, num_to_open, service_level):
    """
    max covering problem : séléctionne les meilleurs emplacements parmi les emplacements donnés selon le nombre max d'installations à ouvrir
    afin de maximiser la couverture des demandes 

    Résout le Max Covering Problem avec distances et niveau de service en utilisant Gurobi.
    
    Arguments :
    - num_installations : nombre d'installations disponibles.
    - num_demands : nombre de demandes à couvrir.
    - distances : matrice de distances (num_demands x num_installations) où distances[i][j] est la distance entre la demande i et l'installation j.
    - num_to_open : nombre d'installations à ouvrir.
    - service_level : distance maximale acceptée pour qu'une installation couvre une demande.
    
    Retour :
    - Les indices des installations à ouvrir pour maximiser la couverture.
    """
    
    # Créer un modèle
    model = grb.Model("MaxCoveringWithDistance")
    
    # Variables de décision
    x = model.addVars(num_installations, vtype=grb.GRB.BINARY, name="x")  # 1 si l'installation j est ouverte
    y = model.addVars(num_demands, num_installations, vtype=grb.GRB.BINARY, name="y")  # 1 si l'installation j couvre la demande i
    
    # Objectif : Maximiser la couverture des demandes
    model.setObjective(grb.quicksum(y[i, j] for i in range(num_demands) for j in range(num_installations)),
                       sense=grb.GRB.MAXIMIZE)
    
    # Contraintes :
    
    # 1. Chaque demande doit être couverte par au moins une installation
    for i in range(num_demands):
        model.addConstr(grb.quicksum(y[i, j] for j in range(num_installations)) >= 1, f"CoverDemand_{i}")
    
    # 2. Limiter le nombre d'installations ouvertes à `num_to_open`
    model.addConstr(grb.quicksum(x[j] for j in range(num_installations)) == num_to_open, "LimitInstallations")
    
    # 3. L'installation j ne peut couvrir la demande i que si elle est ouverte et si la distance est inférieure ou égale à `service_level`
    for i in range(num_demands):
        for j in range(num_installations):
            if distances[i][j] > service_level:  # Si la distance est trop grande, la couverture n'est pas possible
                model.addConstr(y[i, j] == 0, f"DistanceLimit_{i}_{j}")
            model.addConstr(y[i, j] <= x[j], f"Link_y_x_{i}_{j}")
    
    # Résoudre le modèle
    model.optimize()
    
    # Extraire les résultats
    if model.status == grb.GRB.OPTIMAL:
        selected_installations = [j for j in range(num_installations) if x[j].x > 0.5]
        return selected_installations
    else:
        return None

# Entrée utilisateur

# Saisir le nombre d'installations et de demandes
num_installations = int(input("Entrez le nombre d'installations disponibles : "))
num_demands = int(input("Entrez le nombre de demandes à couvrir : "))

# Saisir la matrice des distances
distances = []
for i in range(num_demands):
    distances.append(list(map(int, input(f"Entrez les distances pour la demande {i+1} (séparées par des espaces) : ").split())))

# Saisir le niveau de service (distance maximale acceptable)
service_level = int(input("Entrez le niveau de service (distance maximale acceptable) : "))

# Saisir le nombre d'installations à ouvrir
num_to_open = int(input("Entrez le nombre d'installations à ouvrir : "))

# Résoudre le problème
selected_installations = max_covering_with_distance(num_installations, num_demands, distances, num_to_open, service_level)

# Afficher les résultats
if selected_installations is not None:
    print(f"Installations sélectionnées : {selected_installations}")
else:
    print("Aucune solution optimale n'a été trouvée.")

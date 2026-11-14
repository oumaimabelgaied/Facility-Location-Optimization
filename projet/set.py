import gurobipy as grb

def set_covering_problem_with_distances(num_installations, num_demands, distances, service_levels):
    """
    covering problem : trouve le minimum d'installations pour satisfaire toute les demandes 

    Résout le Set Covering Problem avec des distances et niveaux de service.
    
    Arguments :
    - num_installations : nombre d'installations disponibles.
    - num_demands : nombre de demandes à couvrir.
    - distances : matrice des distances (num_demands x num_installations).
    - service_levels : liste des niveaux de service pour chaque demande (taille num_demands).
    
    Retour :
    - Les indices des installations sélectionnées pour couvrir toutes les demandes.
    """
    
    # Créer un modèle
    model = grb.Model("SetCovering_with_distances")
    
    # Variables de décision
    x = model.addVars(num_installations, vtype=grb.GRB.BINARY, name="x")  # 1 si l'installation j est ouverte
    y = model.addVars(num_demands, num_installations, vtype=grb.GRB.BINARY, name="y")  # 1 si l'installation j couvre la demande i
    
    # Objectif : Minimiser le nombre d'installations ouvertes
    model.setObjective(grb.quicksum(x[j] for j in range(num_installations)),
                       sense=grb.GRB.MINIMIZE)
    
    # Contraintes :
    
    # 1. Chaque demande doit être couverte par au moins une installation
    for i in range(num_demands):
        model.addConstr(grb.quicksum(y[i, j] for j in range(num_installations)) >= 1, f"CoverDemand_{i}")
    
    # 2. Une installation j ne peut couvrir la demande i que si elle est ouverte
    for i in range(num_demands):
        for j in range(num_installations):
            model.addConstr(y[i, j] <= x[j], f"Link_y_x_{i}_{j}")
    
    # 3. Couverture basée sur la distance et le niveau de service
    for i in range(num_demands):
        for j in range(num_installations):
            if distances[i][j] > service_levels[i]:
                model.addConstr(y[i, j] == 0, f"DistanceLimit_{i}_{j}")
    
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

# Saisir la matrice des distances (distances[i][j] = distance entre la demande i et l'installation j)
distances = []
for i in range(num_demands):
    distances.append(list(map(float, input(f"Entrez les distances pour la demande {i+1} (séparées par des espaces) : ").split())))

# Saisir les niveaux de service pour chaque demande
service_levels = list(map(float, input("Entrez les niveaux de service pour chaque demande (séparés par des espaces) : ").split()))

# Résoudre le problème
selected_installations = set_covering_problem_with_distances(num_installations, num_demands, distances, service_levels)

# Afficher les résultats
if selected_installations is not None:
    print(f"Installations sélectionnées : {selected_installations}")
else:
    print("Aucune solution optimale n'a été trouvée.")

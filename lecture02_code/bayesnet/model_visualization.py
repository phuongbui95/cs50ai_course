from pomegranate.distributions import Categorical, ConditionalCategorical

# Node value labels
node_labels = {
    0: ["none", "light", "heavy"],         # Rain
    1: ["yes", "no"],                      # Maintenance
    2: ["on time", "delayed"],             # Train
    3: ["attend", "miss"]                  # Appointment
}

def get_node_name(i):
    """Maps node index to name"""
    names = {0: "Rain", 1: "Maintenance", 2: "Train", 3: "Appointment"}
    return names.get(i, f"Node_{i}")

def print_conditional_probs(dist, node_index):
    """Prints conditional probability tables in a readable format"""
    probs = dist.probs[0]
    shape = probs.shape

    # 2D: One parent
    if len(shape) == 2:
        for i in range(shape[0]):
            formatted_probs = [f"{p:.5f}" for p in probs[i].tolist()]
            # Try to infer parent and outcome labels
            parent_label = node_labels.get(node_index-1, [str(j) for j in range(shape[0])])
            # Example: if node_index = 1 (Maintenance), node_index-1 = 0 (Rain)
            # node_labels[0] = ["none", "light", "heavy"]
            # So parent_label = ["none", "light", "heavy"]
            outcome_label = node_labels.get(node_index, [str(j) for j in range(shape[1])])
            outcome = dict(zip(outcome_label, formatted_probs))
            parent = f"{get_node_name(node_index-1)} = {parent_label[i]}"
            print(f"  {parent}: {outcome}")

    # 3D: Two parents
    elif len(shape) == 3:
        for i in range(shape[0]):
            for j in range(shape[1]):
                formatted_probs = [f"{p:.5f}" for p in probs[i][j]]
                outcome_label = node_labels.get(node_index, [str(k) for k in range(shape[2])])
                outcome = dict(zip(outcome_label, formatted_probs))
                parent1_label = node_labels.get(node_index-2, [str(x) for x in range(shape[0])])
                parent2_label = node_labels.get(node_index-1, [str(y) for y in range(shape[1])])
                parent = f"{get_node_name(node_index-2)} = {parent1_label[i]}, {get_node_name(node_index-1)} = {parent2_label[j]}"
                print(f"  {parent}: {outcome}")

def print_network_structure(model):
    """
    Prints a formatted visualization of the Bayesian Network structure.
    """
    print("\n=== Bayesian Network Structure ===\n")
    for i, dist in enumerate(model.distributions):
        print(f"Node {i}: {get_node_name(i)}")
        if isinstance(dist, Categorical):
            formatted_probs = [f"{p:.5f}" for p in dist.probs.tolist()[0]]
            outcome_label = node_labels.get(i, [str(j) for j in range(len(formatted_probs))])
            print("  Type: Categorical")
            print("  Probabilities:", dict(zip(outcome_label, formatted_probs)))
        elif isinstance(dist, ConditionalCategorical):
            print("  Type: Conditional")
            print("-" * 40)
            print_conditional_probs(dist, i)
        print("-" * 40 + "\n")






'''
#---------------Version 01--------------#

rain = ["none","light","heavy"] # Index 0,1,2
maintenance = ["yes","no"] # Index 0,1
train = ["on time","delayed"] # Index 0,1
appointment = ["attend","miss"] # Index 0,1

def get_node_name(i):
    """Maps node index to name"""
    names = {0: "Rain", 1: "Maintenance", 2: "Train", 3: "Appointment"}
    return names.get(i, f"Node_{i}")

def print_conditional_probs(dist):
    """Prints conditional probability tables in a readable format"""
    probs = dist.probs[0]   
    
    # 2-Dimensional Array
    # row = probs.shape[0], col = probs.shape[1]
    if len(probs.shape) == 2:
        row = probs.shape[0]
        col = probs.shape[1]
        for i in range(probs.shape[0]):
            # print(f"  Given parent={i}: {probs[i].tolist()}")
            formatted_probs = [f"{p:.5f}" for p in probs[i].tolist()]
            outcome = formatted_probs
            parent = i
            if row == 3 and col == 2: # Maintenance
                outcome = dict(zip(maintenance,formatted_probs))
                parent = f"Rain = {rain[i]}"
            elif row == 2 and col == 2: # Appointment
                outcome = dict(zip(appointment,formatted_probs))
                parent = f"Train = {train[i]}"

            print(f"  {parent}: {outcome}")

    # 3-Dimensional Array
    elif len(probs.shape) == 3: # Train
        for i in range(probs.shape[0]):
            for j in range(probs.shape[1]):
                # print(f"  Given parents=({i},{j}): {probs[i][j].tolist()}")
                formatted_probs = [f"{p:.5f}" for p in probs[i][j]]
                outcome = dict(zip(train,formatted_probs))
                parent = f"Rain = {rain[i]}, Maintenance = {maintenance[j]}" 
                # print(f"  Given parents=({i},{j}): {dict(zip(train,formatted_probs))}")
                print(f"  {parent}: {outcome}")

def print_network_structure(model):
    """
    Prints a formatted visualization of the Bayesian Network structure.
    """
    print("\n=== Bayesian Network Structure ===\n")
    
    # Print nodes and their distributions
    for i, dist in enumerate(model.distributions):
        print(f"Node {i}:", get_node_name(i))
        
        if isinstance(dist, Categorical):
            print("Type: Categorical")
            # print("Probabilities:", dist.probs.tolist()[0])
            formatted_probs = [f"{p:.5f}" for p in dist.probs.tolist()[0]]
            print("Probabilities:", dict(zip(rain, formatted_probs)))
            
        elif isinstance(dist, ConditionalCategorical):
            print("Type: Conditional")
            print("Conditional Probability Table:\n"+"-" * 40)
            print_conditional_probs(dist)
            
        print("-" * 40 + "\n")
'''

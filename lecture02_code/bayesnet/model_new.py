''' Re-written from: https://stackoverflow.com/questions/78167360/how-do-i-use-pomegranate-functions '''

from pomegranate.distributions import Categorical, ConditionalCategorical
from pomegranate.bayesian_network import BayesianNetwork
import torch
from model_visualization import print_network_structure

# ------------------------------------Create Nodes------------------------------------

# Rain node has no parents
probs_rain = torch.tensor([
    [   
        0.7,    # none
        0.2,    # light
        0.1     # heavy
    ]    
])
rain = Categorical(probs=probs_rain) # Categorial distribution is a Discrete Distribution

# Track maintenance node is conditional on rain
probs_maintenance = torch.tensor([
    [0.4, 0.6],  # none (rain): yes, no
    [0.2, 0.8],  # light (rain): yes, no
    [0.1, 0.9]   # heavy (rain): yes, no
])
maintenance = ConditionalCategorical(probs=[probs_maintenance])

# Train node is conditional on rain and maintenance
probs_train = torch.tensor([
    [[0.8, 0.2], [0.9, 0.1]],  # "none" (rain): (maintenance) ["yes", "no"] train : on time, delayed
    [[0.6, 0.4], [0.7, 0.3]],  # "light" (rain): (maintenance) ["yes", "no"] train : on time, delayed
    [[0.4, 0.6], [0.5, 0.5]]   # "heavy" (rain): (maintenance) ["yes", "no"] traint\: on time, delayed
])
train = ConditionalCategorical(probs=[probs_train])

# Appointment node is conditional on train
probs_appointment = torch.tensor([
    [0.9, 0.1],  # "on time" (train): attend, miss
    [0.6, 0.4]   # "delayed" (train): attend, miss
])
appointment = ConditionalCategorical(probs=[probs_appointment])

# ------------------------------------Create a Bayesian Network and add states------------------------------------

model = BayesianNetwork()
model.add_distributions([rain, maintenance, train, appointment])

# Add edges connecting nodes
model.add_edge(rain, maintenance)
model.add_edge(rain, train)
model.add_edge(maintenance, train)
model.add_edge(train, appointment)

# Print out Execution
if __name__ == "__main__":
    print(model)
    print_network_structure(model)

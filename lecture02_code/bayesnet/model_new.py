''' Re-written from: https://stackoverflow.com/questions/78167360/how-do-i-use-pomegranate-functions '''

from pomegranate.distributions import Categorical, ConditionalCategorical
from pomegranate.bayesian_network import BayesianNetwork

import torch
from torch.masked import MaskedTensor
from collections import Counter

# ------------------------------------Create Nodes------------------------------------

# Rain node has no parents
probs_rain = torch.tensor([[0.7,    # none
                            0.2,    # light
                            0.1]    # heavy
])
rain = Categorical(probs=probs_rain)

# Track maintenance node is conditional on rain
probs_maintenance = torch.tensor([
    [0.4, 0.6],  # none (rain): yes, no
    [0.2, 0.8],  # light (rain): yes, no
    [0.1, 0.9]   # heavy (rain): yes, no
])
maintenance = ConditionalCategorical(probs=[probs_maintenance])

# Train node is conditional on rain and maintenance
probs_train = torch.tensor([
    [[0.8, 0.2], [0.9, 0.1]],  # "none" (rain): ["yes", "no"] (maintenance): on time, delayed
    [[0.6, 0.4], [0.7, 0.3]],  # "light" (rain): ["yes", "no"] maintenance: on time, delayed
    [[0.4, 0.6], [0.5, 0.5]]   # "heavy" (rain): ["yes", "no"] maintenance: on time, delayed
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

# ------------------------------------Inference Examples------------------------------------

def print_probability_for_observation():
    # Probability for a given observation ["none", "no", "on time", "attend"]
    observation = [0, 1, 0, 0]
    probability = model.probability([observation])
    print("Probability of observation [none, no, on time, attend]:", probability)

def print_predict_proba_for_delayed_train():
    # Predict probabilities given evidence that train was delayed
    observation = torch.tensor([[0, 0, 1, 0]])
    mask = torch.tensor([[False, False, True, False]])
    X = MaskedTensor(observation, mask)
    probabilities = model.predict_proba(X)
    print("Predicted probabilities with train delayed evidence:", probabilities)

# ------------------------------------Rejection Sampling------------------------------------

def rejection_sampling_appointment_given_train_delayed(N=10000):
    # Vectorized sampling for efficiency
    samples = model.sample(N)
    # Filter samples where train is delayed (train index 2 == 1)
    delayed_mask = samples[:, 2] == 1
    delayed_appointments = samples[delayed_mask, 3]
    count = Counter(delayed_appointments.tolist())
    total = sum(count.values())
    prob_attend = count.get(0, 0) / total if total > 0 else 0
    print("Appointment counts given train delayed:", count)
    print(f"Probability that you attend given train is delayed: {prob_attend:.4f}")

# ------------------------------------Main Execution------------------------------------

if __name__ == "__main__":
    print_probability_for_observation()
    print_predict_proba_for_delayed_train()
    rejection_sampling_appointment_given_train_delayed()
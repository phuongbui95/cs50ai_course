from pomegranate.distributions import Categorical
from pomegranate.hmm import DenseHMM
import torch

# Observation model for each state
probs_sun = torch.tensor([
    [
        0.2,   # umbrella
        0.8    # no umbrella
    ]    
])
sun = Categorical(probs=probs_sun)

probs_rain = torch.tensor([
    [
        0.9,   # umbrella
        0.1    # no umbrella
    ]
])
rain = Categorical(probs=probs_rain)

# hidden states
states = [sun, rain]

# Transition model
transitions = [
    [0.8, 0.2], # Tomorrow's predictions if today = sun
    [0.3, 0.7]  # Tomorrow's predictions if today = rain
]

# Starting probabilities
starts = [0.5, 0.5]

# Create the model
model = DenseHMM(states, edges=transitions, starts=starts)

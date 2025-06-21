from pomegranate.distributions import Categorical, ConditionalCategorical
from pomegranate.markov_chain import MarkovChain
import torch
import random

# Define starting probabilities
probs_start = torch.tensor([
    [
        0.5,   # sun
        0.5    # rain
    ]    
])
start = Categorical(probs=probs_start)

# Define transition model
probs_transitions = torch.tensor([
    [0.8, 0.2],  # from sun [start]: to sun, to rain
    [0.3, 0.7]   # from rain [start]: to sun, to rain
])
transitions = ConditionalCategorical(probs=[probs_transitions])

# Create Markov chain
model = MarkovChain([start, transitions])


# Sample 50 states from chain
N = 50
samples = model.sample(N)  # shape: (N, 2)

# # randomly pick starting state
# start_mask_filter = random.randint(0,len(probs_start.tolist())-1)
# start_mask = samples[:, 0] == start_mask_filter


'''
0 in samples[:, 0] is col 1 of each minor array
0 after "==" is index of "sun" in probs_start
samples = [[0, 1],
           [1, 0],
           [0, 0]]
start_mask = [True, False, True]
'''
start_mask = samples[:, 0] == 0  
next_states = samples[start_mask, 1]
'''
samples[:, 0] == 0 creates a boolean mask (start_mask) 
that is True for each row where the first state is 0 (which represents "sun").

samples[start_mask, 1] selects the second state (column 1) from all rows 
where the chain started with "sun".
'''

result = ["sun" if label == 0 else "rain" for label in next_states.tolist()]
print(result)




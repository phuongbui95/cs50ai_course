from pomegranate.distributions import Categorical, ConditionalCategorical
from pomegranate.markov_chain import MarkovChain
import torch

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

# State labels for readability
states = ["sun", "rain"]

# Sample 100 chains of length 2 (start + 1 transition)
N = 100
samples = model.sample(N)  # shape: (N, 2)

# Filter for chains that start from 'sun' (index 0)
sun_start_mask = samples[:, 0] == 0
next_states = samples[sun_start_mask, 1]

# Only keep the first 50 transitions that start from 'sun'
next_states = next_states[:50]

# Convert indices to state labels for readability
next_state_labels = [states[i] for i in next_states.tolist()]

print(len(next_state_labels))  # Should print 50
print(next_state_labels)

'''
# Sample 50 states from chain (if starts from sun, can change if desired)
sample = []
for i in range(100):
    samples = model.sample(1)
    if samples[:, 0] == 0: 
        sample.append(samples[:, 1].item())
print(len(sample)) # should print 50
print(sample)
'''
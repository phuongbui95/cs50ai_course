from model_new import model
import torch
from torch.masked import MaskedTensor

# Define label-to-index mappings
rain = {"none": 0, "light": 1, "heavy": 2}
maintenance = {"yes": 0, "no": 1}
train = {"on time": 0, "delayed": 1}
appointment = {"attend": 0, "miss": 1}

# Predict probabilities given evidence that train was delayed
# Evidence: train is delayed (index 2 is 1), others are unknown
# predictions = torch.tensor([[0,0,1,0]])
evidence = torch.tensor([[0, 0, train["delayed"], 0]])  # Values are placeholders except for train
mask = torch.tensor([[False, False, True, False]])      # Only train is observed

X = MaskedTensor(evidence, mask)
probabilities = model.predict_proba(X)

## Print out
print("\nPredicted probabilities given evidence that train was delayed:")

nodes = [
    ("Rain", ["none", "light", "heavy"]),
    ("Maintenance", ["yes", "no"]),
    ("Train", ["on time", "delayed"]),
    ("Appointment", ["attend", "miss"])
]

for i, node_probs in enumerate(probabilities): # enumerate: The enumerate object yields pairs: a count and a value yielded by the iterable argument.
    name, value_labels = nodes[i]
    flat_list_of_probs = node_probs.tolist()[0]
    formatted_value = {value_labels[j]: f"{prob:.4f}" for j, prob in enumerate(flat_list_of_probs)}
    print(f"{name}: {formatted_value}")
from model_new import model
import torch
from torch.masked import MaskedTensor

# Predict probabilities given evidence that train was delayed
observation = torch.tensor([[0, 0, 1, 0]]) # ["none", "no", "delayed", "attend"]
mask = torch.tensor([[False, False, True, False]])
X = MaskedTensor(observation, mask)
probabilities = model.predict_proba(X)

print(probabilities)

'''
# Print predictions for each node
for node, prediction in zip(model.states, predictions):
    if isinstance(prediction, str):
        print(f"{node.name}: {prediction}")
    else:
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"    {value}: {probability:.4f}")
'''
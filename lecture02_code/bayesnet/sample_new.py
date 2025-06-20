from collections import Counter
from model_new import model

# Define label-to-index mappings
rain = {"none": 0, "light": 1, "heavy": 2}
maintenance = {"yes": 0, "no": 1}
train = {"on time": 0, "delayed": 1}
appointment = {"attend": 0, "miss": 1}

# Vectorized sampling for efficiency
N = 10000 # int(input('Enter sample size:'))

# Draw samples: each row is [rain, maintenance, train, appointment]
samples = model.sample(N)

# Filter samples where train is delayed
# samples[:,2] = select the third variable ("train") from all samples
node_name = {"rain":0, "maintenance":1, "train":2, "appointment":3}
delayed_train_mask = samples[:, node_name["train"]] == train["delayed"]
appointments_outcome = samples[delayed_train_mask, node_name["appointment"]]

# Count Appointment Outcomes
counts = Counter(appointments_outcome.tolist())
total = sum(counts.values())
prob_attend = counts.get(appointment["attend"], 0) / total if total > 0 else 0 # prob_attend = count.get(0, 0) / total if total > 0 else 0

# Print results with labels
label_map = {0: "attend", 1: "miss"}
formatted_counts = {label_map.get(k, str(k)): v for k, v in counts.items()}

print("Appointment counts given train delayed:", formatted_counts)
print(f"Probability that you attend given train is delayed: {prob_attend:.4f}")
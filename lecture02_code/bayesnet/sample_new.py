from collections import Counter
from model_new import model

# Vectorized sampling for efficiency
N = 10000 # int(input('Enter sample size:'))
samples = model.sample(N)
# Filter samples where train is delayed (train index 2 == 1)
delayed_mask = samples[:, 2] == 1
delayed_appointments = samples[delayed_mask, 3]
count = Counter(delayed_appointments.tolist())
total = sum(count.values())
prob_attend = count.get(0, 0) / total if total > 0 else 0
print("Appointment counts given train delayed:", count)
print(f"Probability that you attend given train is delayed: {prob_attend:.4f}")

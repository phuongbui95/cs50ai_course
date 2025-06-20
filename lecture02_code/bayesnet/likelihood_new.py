from model_new import model

# Define label-to-index mappings
rain = {"none": 0, "light": 1, "heavy": 2}
maintenance = {"yes": 0, "no": 1}
train = {"on time": 0, "delayed": 1}
appointment = {"attend": 0, "miss": 1}

# Probability for a given observation ["none", "no", "on time", "attend"]
# The order is defined in the model (rain -> maintenance -> train -> appointment)
# brief version: observation = [0, 1, 0, 0] 
observation = [
    rain["none"],           # return 0
    maintenance["no"],      # return 1
    train["on time"],       # return 0
    appointment["attend"]   # return 0
]

probability = model.probability([observation])
print(probability)

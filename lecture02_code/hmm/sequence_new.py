from model_new import model
import numpy

# Observed data
observations = numpy.array([
    [
        [0],[0],[1],[0],[0],[0],[0],[1],[1] # 0: umbrella, 1: no umbrella
    ]
])

# Predict underlying states
predictions = model.predict(observations)
# convert indices to readable texts
X = list()
for prediction in predictions.tolist()[0]:
    # hidden states: {0: sun, 1: rain}
    X.append("rain") if prediction == 1 else X.append("sun")

print(X) 

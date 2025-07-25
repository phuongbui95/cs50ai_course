import tensorflow as tf
import cv2
import numpy as np

# Load the saved model
model = tf.keras.models.load_model('model.keras')

def predict_sign(image_path):
    # Read and preprocess the image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (30, 30))  # Match IMG_WIDTH and IMG_HEIGHT
    img = np.array([img]) / 255.0  # Normalize and add batch dimension
    
    # Get prediction
    prediction = model.predict(img)
    return np.argmax(prediction[0])

# Test the model
test_image = "/home/phuongbui/cs50/cs50ai_course/traffic/gtsrb-small/0/00000_00000.ppm"
result = predict_sign(test_image)
print(f"Predicted traffic sign category: {result}")
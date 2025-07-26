import cv2
import numpy as np
import os
import sys
import tensorflow as tf

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43 # only 3 if gtsrb-small
# NUM_CATEGORIES_SMALL = 3
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.keras]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]

        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """
    images = list()
    labels = list()

    for category in os.listdir(data_dir):
        try:
            category_path = os.path.join(data_dir, category)
            # continue if directory is empty
            if not os.path.isdir(category_path):
                continue
            
            # Process each image in category folder
            for image_file in os.listdir(category_path):
                try:
                    image_path = os.path.join(category_path, image_file)
                    img = cv2.imread(image_path)
                    # continue with warning if cannot read the image file
                    if img is None:
                        print(f"Warning: Could not read image {image_path}")
                        continue

                    resized_img = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT))
                    images.append(resized_img)
                    # normalized_img = resized_img / 255.0  # Normalize pixel values
                    # images.append(normalized_img)
                    labels.append(int(category))
                
                except Exception as e:
                    print(f"Error processing {image_file}: {e}")
                    continue
        except ValueError:
            print(f"Warning: Invalid category name {category}")
            continue

    return (images, labels)

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    # Create a convolutional neural network
    input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)
    # filters: 32, 64, 128
    # Basic CNN Structure: Conv2D → MaxPooling → Dropout → Flatten → Dense
    model = tf.keras.models.Sequential([

        # First conv block
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu", input_shape=input_shape),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        
        # Second conv block
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
        
        # Third conv block
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        # Other layers and setup
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(NUM_CATEGORIES, activation="softmax")
    ])

    # Train neural network
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

if __name__ == "__main__":
    main()
    # images, labels = load_data("gtsrb-small")
    # print(f"Loaded {len(images)} images")
    # print(f"Image shape: {images[0].shape}")
    # print(f"Pixel value range: {images[0].min():.2f} to {images[0].max():.2f}")

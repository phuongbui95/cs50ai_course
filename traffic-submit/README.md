# Traffic Sign Classification Project

## Experimental Results

### 1. Basic Model with Single Conv Layer
- Architecture: 1x Conv2D(32) → MaxPooling → Dropout → Flatten → Dense
- Initial accuracy: ~55%
- Key finding: Poor performance due to lack of image normalization

### 2. Added Image Normalization
- Architecture: Same as Experiment 1
- Changes made: Added image normalization (pixel values / 255.0)
- Results:
  - Accuracy: 97%
  - Significant improvement from baseline

### 3. Added Second Conv Layer
- Architecture: Conv2D(32) → MaxPooling → Conv2D(64) → MaxPooling → Dropout → Flatten → Dense
- Results:
  - Accuracy: 96%
  - Speed: 9ms/step (compared to 7ms in Experiment 2)
  - Slight accuracy decrease in comparison to Experiment 2

### 4. Three Conv Layer Model
- Architecture: Conv2D(32) → MaxPooling → Conv2D(64) → MaxPooling → Conv2D(128) → MaxPooling → Dropout → Flatten → Dense
- Results:
  - Similar accuracy to Experiment 3
  - Similar processing speed to Experiment 3

## Key Learnings
1. Image normalization is crucial for model performance
2. Adding more convolutional layers doesn't always improve accuracy
3. Model complexity trades off with processing speed
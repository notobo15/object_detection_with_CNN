from tensorflow.keras import models
import cv2
import os
import numpy as np
from pathlib import Path
PROJECT_PATH = Path(os.path.abspath(os.path.dirname(__file__))).resolve().parent
parent_dir = os.path.join(PROJECT_PATH, 'static', 'uploads', 'd813f589-d0d3-4df7-938e-2ca494c45987')
print(PROJECT_PATH)
print(parent_dir)
# Load the model
my_model = models.load_model(os.path.join(parent_dir, 'model.keras'))

# Read the image in grayscale // 
# image = cv2.imread(os.path.join(PROJECT_PATH, 'test', 'airphane.jpg'), cv2.IMREAD_UNCHANGED)
# image = cv2.imread(os.path.join(PROJECT_PATH, 'test', 'dog.webp'), cv2.IMREAD_UNCHANGED)
image = cv2.imread(os.path.join(PROJECT_PATH, 'test', 'dog1.jpg'), cv2.IMREAD_UNCHANGED)

# Resize the image to (32, 32)
image = cv2.resize(image, (32, 32))
# image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
# Normalize the pixel values to the range [0, 1]
image = image / 255.0

# Add a channel dimension
# image = np.expand_dims(image, axis=-1)  # Now image shape is (32, 32, 1)

# Add a batch dimension
image = np.expand_dims(image, axis=0)   # Now image shape should be (1, 32, 32, 1)

# Predict using the model
result = my_model.predict(image)
print(result)

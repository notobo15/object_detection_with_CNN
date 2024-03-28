import numpy as np
import os
from PIL import Image
import tensorflow as tf
from tensorflow.keras import models, layers
from tensorflow.keras.utils import to_categorical 
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
class Traning:
  def __init__(self, uuid):
    self.uuid = uuid 
    self.uuid_path = os.path.join(PROJECT_PATH, 'uploads', uuid)
   
  def getData(self, dirData):
    list_data = []
    classes = {label: idx for idx, label in enumerate(os.listdir(dirData))}
    for folder in os.listdir(dirData):
        
      folder_path = os.path.join(dirData, folder)
      for filename in os.listdir(folder_path):
          filename_path = os.path.join(folder_path, filename)
          img = Image.open(filename_path).resize((32, 32))  # Đảm bảo ảnh đúng kích thước
          img = np.array(img)
          if img.shape == (32, 32, 3):  # Chỉ xử lý ảnh RGB
              list_data.append((img, classes[folder]))  # Sử dụng folder làm label
    return list_data

  # def getData(self, dirData):
  #   list_data = []
  #   for folder in os.listdir(dirData):
  #       folder_path = os.path.join(dirData, folder)
  #       list_filename_path = []
  #       classes = {os.listdir(folder_path): idx for idx, label in enumerate(list(os.listdir(folder_path)))}
  #       for filename in os.listdir(folder_path):
  #           filename_path = os.path.join(folder_path, filename)
  #           label = filename_path.split('\\')[-2]
  #           img = np.array(Image.open(filename_path))
  #           list_filename_path.append((img, classes[label]))
  #       list_data.extend(list_filename_path)
  #   return list_data

  def testing(self):
    path = self.uuid_path
    print(path)
    train_data = self.getData(path)
    # test_data = getData(TEST_DATA)
    Xtrain = np.array([x[0] for x in train_data])
    Ytrain = np.array([y[1] for y in train_data])

    Xtest = []
    Ytest = []
    model_training = models.Sequential([
    layers.Conv2D(32, (3, 3), input_shape=(32,32,3), activation='relu'),
    layers.MaxPool2D((2,2)),
    layers.Dropout(0.15),

    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPool2D((2, 2)),
    layers.Dropout(0.2),

    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPool2D((2, 2)),
    layers.Dropout(0.2),


    layers.Flatten(),
    layers.Dense(1000, activation='relu'),
    layers.Dense(256, activation='relu'),
    layers.Dense(2, activation='softmax'),
    ])
    # model_training.summary()

    model_training.compile(optimizer='adam', loss='categorical_crossentropy', metrics = ['accuracy'])
    Ytrain_one_hot = to_categorical(Ytrain, num_classes=2)
    model_training.fit(Xtrain, Ytrain_one_hot, epochs=10)

    # model_training.save(os.path.join(self.uuid_path, f"{self.uuid}-model.keras"))
    model_training.save(f"model-v1.h5")



test1 = Traning('ce1bd24590af4e73838dc49710f36a6a')
test1.testing()

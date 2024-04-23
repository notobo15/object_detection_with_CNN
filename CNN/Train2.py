
import os
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import tensorflowjs as tfjs
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from tensorflow.keras.layers import LeakyReLU
from tensorflow.keras.utils import to_categorical
from . import Setting
class Building:
    def __init__(self, data_dir, img_height, img_width, num_classes, class_names,epochs,patch_sizes,optimizer,test_size ):
        self.data_dir = data_dir
        self.img_height = img_height
        self.img_width = img_width
        self.num_classes = num_classes
        self.class_names = class_names
        self.epochs = epochs
        self.patch_sizes = patch_sizes
        self.optimizer = optimizer
        self.test_size = test_size

    def _read_data(self):
        # class_names = os.listdir(self.data_dir)
        class_names = self.class_names
        images = []
        labels = []

        for label, class_name in enumerate(class_names):
            class_dir = os.path.join(self.data_dir, class_name)
            print(class_dir)
            for image_name in os.listdir(class_dir):
                image_path = os.path.join(class_dir, image_name)
                image = tf.io.read_file(image_path)
                image = tf.image.decode_image(image, channels=3)
                image = tf.image.resize(image, [self.img_height, self.img_width])
                images.append(image)
                labels.append(label)
                    
        self.images = np.array(images)
        self.labels = np.array(labels)

    def _preprocess_data(self):
        self.images = self.images / 255.0

    def build_model(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
            tf.keras.layers.MaxPooling2D(2, 2),
             tf.keras.layers.Dropout(0.15),


            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Dropout(0.2),


            tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Dropout(0.2),

            # tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            # tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(1000, activation='relu'),
            # tf.keras.layers.Dense(500, activation='relu'),
            tf.keras.layers.Dense(256, activation='relu'),
            # tf.keras.layers.Dense(128, activation='relu'),

            tf.keras.layers.Dense(20, activation='softmax'),
            tf.keras.layers.Dense(self.num_classes, activation='softmax')

            # tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(self.img_height, self.img_width, 3)),
            # tf.keras.layers.MaxPooling2D(2, 2),
            # tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            # tf.keras.layers.MaxPooling2D(2, 2),
            # tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
            # tf.keras.layers.MaxPooling2D(2, 2),
            # tf.keras.layers.Flatten(),
            # tf.keras.layers.Dense(512, activation='relu'),
            # tf.keras.layers.Dropout(0.5),
            # tf.keras.layers.Dense(self.num_classes, activation='softmax')
        ])
        self.model.compile(optimizer='adam',
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])


    def build_model2(self):
        self.model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(16, (3, 3), input_shape=(self.img_height, self.img_width, 3)),
            LeakyReLU(alpha=0.1),  # Sử dụng Leaky ReLU thay vì ReLU
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(32, (3, 3)),
            LeakyReLU(alpha=0.1),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3)),
            LeakyReLU(alpha=0.1),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(1000),
            LeakyReLU(alpha=0.1),
            tf.keras.layers.Dense(256),
            LeakyReLU(alpha=0.1),
            tf.keras.layers.Dense(128),
            LeakyReLU(alpha=0.1),
            # tf.keras.layers.Dense(20, activation='softmax'),
            tf.keras.layers.Dense(self.num_classes, activation='softmax')
        ])
        self.model.compile(optimizer=self.optimizer,
                           loss='sparse_categorical_crossentropy',
                           metrics=['accuracy'])
    def train(self, test_size=0.2, epochs=20):
        self._read_data()
        self._preprocess_data()
        # train_images, test_images, train_labels, test_labels = train_test_split(self.images, self.labels,
        #                                                                         test_size=test_size, random_state=42)
        # self.model.fit(train_images, train_labels, epochs=epochs, validation_data=(test_images, test_labels))
        # self.test_images = test_images
        # self.test_labels = test_labels  # Lưu lại test_images và test_labels

        train_images, test_images, train_labels, test_labels = train_test_split(self.images, self.labels, test_size=test_size, random_state=None)
        self.model.fit(train_images, train_labels, epochs=epochs)

    def train2(self):
        self._read_data()
        self._preprocess_data()
        train_images, test_images, train_labels, test_labels = train_test_split(
            self.images, self.labels, test_size=self.test_size, random_state=42
        )
        self.test_images = test_images  # Save test images for evaluation
        self.test_labels = test_labels  # Save test labels for evaluation
        self.model.fit(
            train_images, train_labels,
            epochs=self.epochs,
            validation_data=(test_images, test_labels),
            batch_size=self.patch_sizes
        )
    def evaluate(self):
        test_loss, test_acc = self.model.evaluate(self.test_images, self.test_labels, verbose=2)  # Sử dụng test_images và test_labels đã lưu
        print('\nTest accuracy:', test_acc)

    def save_model(self, model_path='model'):
        # logger.info(os.path.join(self.data_dir,'model'))
        # self.model.save(os.path.join(self.data_dir, "model.keras"))
        tfjs.converters.save_keras_model(self.model, self.data_dir)
        # self.model.save(os.path.join(self.data_dir, model_path))


       
# PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
# parent_dir = os.path.join(PROJECT_PATH, 'static', 'uploads', '60ee7202-6186-44c9-8607-437f5a681e82')
       
# img_height = 28
# img_width = 28
# num_classes = len(os.listdir(parent_dir))

# classifier = ImageClassifier(parent_dir, img_height, img_width, num_classes)
# classifier.build_model()
# classifier.train()

# classifier.evaluate()
# classifier.save_model()
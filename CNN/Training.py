import cv2
from keras.applications.mobilenet import MobileNet
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.models import Model
import tensorflowjs as tfjs
from keras.preprocessing.image import ImageDataGenerator
import keras
from keras.callbacks import ModelCheckpoint
import os
class FlowerClassifier:
    def __init__(self, n_class=5):
        self.n_class = n_class
        self.model = None
        self.size = 32

    def build_model(self):
        base_model = MobileNet(include_top=False, weights="imagenet", input_shape=(self.size,self.size,3))
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.25)(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.25)(x)
        x = Dense(512, activation='relu')(x)
        outs = Dense(self.n_class, activation='softmax')(x)

        for layer in base_model.layers:
            layer.trainable = False

        self.model = Model(inputs=base_model.inputs, outputs=outs)

    def make_data(self, data_folder="flower_images_raw", batch_size=64):
        train_datagen = ImageDataGenerator(preprocessing_function= keras.applications.mobilenet.preprocess_input,rotation_range=0.2,
                                           width_shift_range=0.2,   height_shift_range=0.2,shear_range=0.3,zoom_range=0.5,
                                           horizontal_flip=True, vertical_flip=True,
                                           validation_split=0.2)

        train_generator = train_datagen.flow_from_directory(data_folder,
                                                            target_size=(self.size, self.size),
                                                            batch_size=batch_size,
                                                            class_mode='categorical',
                                                            subset='training')

        validation_generator = train_datagen.flow_from_directory(
            data_folder,  # same directory as training data
            target_size=(self.size, self.size),
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation')  # set as validation data

        return train_generator, validation_generator

    def train_model(self, train_generator, validation_generator, n_epochs=10):
        self.model.compile(optimizer='sgd', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

        # checkpoint = ModelCheckpoint('models/best.hdf5', monitor='val_loss', save_best_only = True, mode='auto')
        # callback_list = [checkpoint]

        step_train = train_generator.n//train_generator.batch_size
        step_val = validation_generator.n//validation_generator.batch_size

        self.model.fit_generator(generator=train_generator, steps_per_epoch=step_train,
                                 validation_data=validation_generator,
                                 validation_steps=step_val,
                                #  callbacks=callback_list,
                                 epochs=n_epochs)

    def save_model(self, save_path='result'):
        tfjs.converters.save_keras_model(self.model, save_path)


# PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
# folder = os.path.join(PROJECT_PATH, 'static', 'uploads', 'ce1bd24590af4e73838dc49710f36a6a')
# flower_classifier = FlowerClassifier()
# flower_classifier.build_model()
# train_generator, validation_generator = flower_classifier.make_data(folder)
# flower_classifier.train_model(train_generator, validation_generator)
# flower_classifier.save_model(folder)
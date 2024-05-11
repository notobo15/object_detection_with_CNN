import cv2
from keras.applications.mobilenet import MobileNet
from keras.layers import GlobalAveragePooling2D, Dense, Dropout, GlobalMaxPooling2D
from keras.models import Model
import tensorflowjs as tfjs
from keras.preprocessing.image import ImageDataGenerator
import keras
from keras.callbacks import ModelCheckpoint
import os
import matplotlib.pyplot as plt
import numpy as np
class Training:
    def __init__(self, size=112, epochs=20, patch_sizes=64, optimizer='adam', loss='categorical_crossentropy', test_size=0.2, num_classes=0, folder_path='',PoolingType = 'AveragePooling'):
        self.model = None
        self.size = size
        self.epochs = epochs
        self.patch_sizes = patch_sizes
        self.optimizer = optimizer
        self.loss = loss
        self.num_classes = num_classes
        self.test_size = test_size
        self.folder_path = folder_path
        self.PoolingType = PoolingType
        self.history = None
        self.folder_train_path = None

    def build_model(self):
        base_model = MobileNet(include_top=False, weights="imagenet", input_shape=(self.size,self.size,3))
        x = base_model.output
        if self.PoolingType == 'MaxPooling':
             x = GlobalMaxPooling2D()(x)
        else:
            x = GlobalAveragePooling2D()(x)

        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.25)(x)
        x = Dense(256, activation='relu')(x)
        x = Dropout(0.2)(x)

        outs = Dense(self.num_classes, activation='softmax')(x)

        for layer in base_model.layers:
            layer.trainable = False

        self.model = Model(inputs=base_model.inputs, outputs=outs)

    def make_data(self):
        train_datagen = ImageDataGenerator(preprocessing_function= keras.applications.mobilenet.preprocess_input,rotation_range=0.2,
                                           width_shift_range=0.2,   height_shift_range=0.2,shear_range=0.3,zoom_range=0.5,
                                           horizontal_flip=True, vertical_flip=True,
                                           validation_split=self.test_size)

        train_generator = train_datagen.flow_from_directory(self.folder_path,
                                                            target_size=(self.size, self.size),
                                                            batch_size=self.patch_sizes,
                                                            class_mode='categorical',
                                                            subset='training')

        validation_generator = train_datagen.flow_from_directory(
            self.folder_path,  # same directory as training data
            target_size=(self.size, self.size),
            batch_size=self.patch_sizes,
            class_mode='categorical',
            subset='validation')  # set as validation data

        return train_generator, validation_generator

    def train_model(self, train_generator, validation_generator):
        self.model.compile(optimizer=self.optimizer, loss=self.loss, metrics=['accuracy'])
        self.model_checkpoint_path = os.path.join(self.folder_path,'best.hdf5') 
        checkpoint = ModelCheckpoint(self.model_checkpoint_path, monitor='val_loss', save_best_only=True, mode='auto')
        callback_list = [checkpoint]
        
        # step_train = train_generator.n//train_generator.batch_size
        # step_val = validation_generator.n//validation_generator.batch_size

        # self.model.fit_generator(generator=train_generator, steps_per_epoch=len(train_generator),
        #                         validation_data=validation_generator,
        #                         validation_steps=len(validation_generator),
        #                         callbacks=callback_list,
        #                         epochs=self.epochs)

        self.history = self.model.fit(train_generator, steps_per_epoch=len(train_generator),
               validation_data=validation_generator, validation_steps=len(validation_generator),
               callbacks=callback_list, epochs=self.epochs)

    def delete_model_checkpoint(self):
        if os.path.exists(self.model_checkpoint_path):
            os.remove(self.model_checkpoint_path)

    def save_model(self):
        tfjs.converters.save_keras_model(self.model, self.folder_path)
        self.delete_model_checkpoint()

        self.plot_training_history()


    def plot_training_history(self):
        # Lấy các giá trị loss và accuracy từ history
        history = self.history
        # epochs = self.epochs
        train_loss = history.history['loss']
        val_loss = history.history['val_loss']
        train_acc = history.history['accuracy']
        val_acc = history.history['val_accuracy']
        epochs = range(1, len(train_loss) + 1)
        epochs_val = range(1, len(val_loss) + 1)

        # Vẽ đồ thị
        plt.figure(figsize=(10, 5))
        plt.subplot(1, 2, 1)
        plt.plot(epochs, train_loss, label='Training Loss')
        plt.plot(epochs_val, val_loss, label='Validation Loss')
        plt.title('Training and Validation Loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(epochs, train_acc, label='Training Accuracy')
        plt.plot(epochs, val_acc, label='Validation Accuracy')
        plt.title('Training and Validation Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()

        plt.tight_layout()
                    
        if self.folder_path is not None:
            plt.savefig(os.path.join(self.folder_path, 'analyst.png'))
        
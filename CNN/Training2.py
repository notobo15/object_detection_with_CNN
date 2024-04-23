import tensorflow as tf
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam

class FlowerClassifier:
    def __init__(self, n_class=10):
        self.n_class = n_class
        self.model = None
        self.size = 32  # Giữ nguyên cho CIFAR-10

    def build_model(self):
        base_model = MobileNet(include_top=False, weights="imagenet", input_shape=(self.size, self.size, 3))
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.5)(x)  # Tăng dropout
        x = Dense(512, activation='relu')(x)
        outs = Dense(self.n_class, activation='softmax')(x)

        # Để tinh chỉnh, bạn có thể sau này mở khóa một số lớp để huấn luyện
        for layer in base_model.layers:
            layer.trainable = False

        self.model = Model(inputs=base_model.inputs, outputs=outs)
        self.model.compile(optimizer=Adam(lr=0.0001), loss='categorical_crossentropy', metrics=['accuracy'])

    def train_model(self, train_generator, validation_generator, n_epochs=20):
        early_stop = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min')
        model_checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, mode='max')

        step_train = train_generator.n // train_generator.batch_size
        step_val = validation_generator.n // validation_generator.batch_size

        self.model.fit(train_generator,
                       steps_per_epoch=step_train,
                       validation_data=validation_generator,
                       validation_steps=step_val,
                       epochs=n_epochs,
                       callbacks=[early_stop, model_checkpoint])

# Sử dụng CIFAR-10 dataset
(x_train, y_train), (x_val, y_val) = tf.keras.datasets.cifar10.load_data()

# Preprocessing và Data Augmentation
train_datagen = ImageDataGenerator(
    preprocessing_function=tf.keras.applications.mobilenet.preprocess_input,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest',
    validation_split=0.2)

# train_generator = train_datagen.flow(x_train, y_train, batch_size=64, subset='training')
# validation_generator = train_datagen.flow(x_train, y_train, batch_size=64, subset='validation')

# # Khởi tạo và huấn luyện mô hình
# flower_classifier = FlowerClassifier(10)  # CIFAR-10 có 10 classes
# flower_classifier.build_model()
# flower_classifier.train_model(train_generator, validation_generator)

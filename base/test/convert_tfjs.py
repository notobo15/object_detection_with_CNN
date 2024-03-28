import os
import tensorflowjs as tfjs
from tensorflow.keras.models import load_model

def convert_h5_to_tfjs(source_dir, dest_dir):
    # Tạo thư mục đích nếu nó chưa tồn tại
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Duyệt qua tất cả các file trong thư mục nguồn
    for filename in os.listdir(source_dir):
        if filename.endswith(".h5"):
            # Đường dẫn đầy đủ tới file nguồn và đích
            source_path = os.path.join(source_dir, filename)
            model_name = os.path.splitext(filename)[0]
            dest_path = os.path.join(dest_dir, model_name)

            # Tải và chuyển đổi mô hình
            model = load_model(source_path)
            tfjs.converters.save_keras_model(model, dest_path)
            print(f"Converted {filename} to TensorFlow.js format.")

# Đặt đường dẫn của bạn ở đây
source_dir = "C:\\Users\\chris\\OneDrive\Desktop\\cnn-python\\Testing\\model-cifar100-v1.h5"
dest_dir = 'C:\\Users\\chris\\OneDrive\Desktop\\cnn-python\\Testing\\tfjs_models'

convert_h5_to_tfjs(source_dir, dest_dir)

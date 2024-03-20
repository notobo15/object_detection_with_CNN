from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import models

from tensorflow.keras.datasets import cifar10
import base64
import numpy as np
# import tensorflow as tf
# # import matplotlib.pyplot as plt
# import numpy as np
# import io
# import base64
# from PIL import Image


def home(request):
    return render(request, 'home.html')

def train(request):
    return render(request, 'train.html') 

def standardTraining(request, detail):

   
    (_, _), (x_test, _) = cifar10.load_data()

    # Chọn một hình ảnh từ tập dữ liệu kiểm tra (ví dụ: hình ảnh đầu tiên)
    image = x_test[0]

    # Chuyển đổi hình ảnh sang dạng dữ liệu Base64
    image_base64 = base64.b64encode(image).decode('utf-8')
    labels = models.Label.objects.all()
    return render(request, 'standard_training.html', {'labels':labels, 'image_base64': image_base64})



datasets = [
    {
        "name": "MNIST",
        "description": "A dataset containing 70,000 grayscale images of handwritten digits 0-9, widely used for training and testing in the field of machine learning for image recognition."
    },
    {
        "name": "CIFAR-10",
        "description": "A dataset consisting of 60,000 32x32 color images in 10 classes, with 6,000 images per class, including airplanes, cars, birds, cats, etc."
    },
    {
        "name": "ImageNet",
        "description": "A large image database used for deep learning model training, containing over 14 million labeled images across roughly 20,000 categories."
    },
    {
        "name": "Fashion-MNIST",
        "description": "A dataset comprising 70,000 grayscale images of 10 fashion categories such as t-shirts, trousers, shoes, bags, etc., each of 28x28 pixel resolution."
    },
    {
        "name": "CIFAR-100",
        "description": "Similar to CIFAR-10 but with 100 classes. Each class contains 600 color images of 32x32 pixels, for a total of 60,000 images."
    },
    {
        "name": "TensorFlow Speech Commands",
        "description": "A dataset containing about 105,000 one-second audio files of thousands of people saying 35 different words such as 'yes', 'no', 'up', 'down', and more."
    },
    {
        "name": "CORe50",
        "description": "A dataset for Continual Object Recognition containing 50 different objects recorded in various settings, lighting, and angles."
    },
    {
        "name": "DeepFashion",
        "description": "A dataset featuring over 800,000 labeled images, including fashion styles, types of clothing, and information on the location of each item on the body."
    }
]

def standardTrainingDatasets(request, detail):
    print(detail)
    return render(request, 'standard_training_datasets.html', {'datasets': datasets})

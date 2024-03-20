from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from . import models
import numpy as np
import logging
import os

def home(request):
    return render(request, 'home.html')

def train(request):
    return render(request, 'train.html') 

def standardTraining(request, detail):

    logger = logging.getLogger('django')

    logger.info('here goes your message')

    labels = models.Label.objects.all()

      # Tạo một từ điển để lưu trữ các hình ảnh cho mỗi nhãn
    images_by_label = {}

    # Duyệt qua từng nhãn và lấy 10 hình ảnh cho mỗi nhãn
    for label in labels:
        images = models.Image.objects.filter(label=label)[:10]  # Lấy 10 hình ảnh đầu tiên cho mỗi nhãn
        images_by_label[label] = images
        logger.info(images)


    return render(request, 'standard_training.html', {'labels': labels, 'images_by_label': images_by_label})

# # Thêm các nhãn vào cơ sở dữ liệu
#     for i, class_name in enumerate(class_names):
#         label, created = models.Label.objects.get_or_create(name=class_name, index=i)

#     # Thêm các ảnh vào cơ sở dữ liệu với nhãn từ 0 đến 9
#     for class_name in class_names:
#         class_dir = os.path.join(cifar10_dir, class_name)
#         label = models.Label.objects.get(name=class_name)

#         image_files = os.listdir(class_dir)
#         for image_file in image_files:
#             # Thêm tên ảnh vào cơ sở dữ liệu
#             image_name = os.path.splitext(image_file)[0]
#             models.Image.objects.create(name=image_name, label=label)


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

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

    labels = models.Label.objects.all()

    # Tạo một danh sách để lưu trữ các cặp nhãn và danh sách hình ảnh tương ứng
    images_by_labels = []

    # Lặp qua từng nhãn và lấy danh sách hình ảnh tương ứng
    for label in labels:
        images = models.Image.objects.filter(label=label)[:100]
        images_by_labels.append((label, images))

    return render(request, 'standard_training.html', {'images_by_labels': images_by_labels})

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



def standardTrainingDatasets(request, detail):


    return render(request, 'standard_training_datasets.html')

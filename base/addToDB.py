import os
from base import  models
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
folder_dataset = os.path.join(PROJECT_PATH, 'static', 'datasets', 'mnist')
class_names = os.listdir(folder_dataset)

for i, class_name in enumerate(class_names):
    label, created = models.Label.objects.get_or_create(name=class_name, index=i)

# Thêm các ảnh vào cơ sở dữ liệu với nhãn từ 0 đến 9
for class_name in class_names:
    class_dir = os.path.join(folder_dataset, class_name)
    label = models.Label.objects.get(name=class_name)

    image_files = os.listdir(class_dir)
    for image_file in image_files:
        # Thêm tên ảnh vào cơ sở dữ liệu
        image_name = os.path.splitext(image_file)[0]
        models.Image.objects.create(name=image_name, label=label)
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from . import models
import numpy as np
import logging
import os
import cv2
def home(request):
    return render(request, 'home.html')

def getting_started(request):
    return render(request, 'getting_started.html')

def train(request):
    return render(request, 'train.html') 

logger = logging.getLogger('django')

def standardTrainingDetail(request, slug):

    dataset = models.Dataset.objects.filter(slug=slug).first()
    labels = models.Label.objects.filter(dataset=dataset)

    # Tạo một danh sách để lưu trữ các cặp nhãn và danh sách hình ảnh tương ứng
    images_by_labels = []

    # Lặp qua từng nhãn và lấy danh sách hình ảnh tương ứng
    for label in labels:
        images = models.Image.objects.filter(label=label)[:10]
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



def standardTraining(request):

    datasets = models.Dataset.objects.all()
    

    return render(request, 'standard_training_datasets.html', {'datasets': datasets})

def stream(request):
    return render(request, 'stream.html')

def stream():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed camera")
            break
        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image_bytes + b'\r\n')  


def video(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')   






import json
import os
import cv2
from PIL import Image
import numpy as np
import uuid
import tensorflow as tf
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
class CustomFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name

class PredictImageView(APIView):
    def get(self, request):
        return HttpResponse("test")
    def post(self, request):
        serializer = ImageSerializer(data=request.data)

        if serializer.is_valid():
            image = serializer.validated_data['image']
            dataset = serializer.validated_data['dataset']
            logger.info(image)
            fss = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "tmp"))
            try:
                unique_filename = str(uuid.uuid4()) + ".jpg"  # Ví dụ sử dụng UUID
                _image = fss.save(unique_filename, image)
                path = os.path.join(str(settings.MEDIA_ROOT), '\\tmp', unique_filename)
                # image details
                image_url = fss.url(_image)
                # Read the image
                imag=cv2.imread(os.getcwd() + path)

                if imag is not None:
                    img_from_ar = Image.fromarray(imag, 'RGB')
                    resized_image = img_from_ar.resize((32, 32))

                    test_image = np.expand_dims(resized_image, axis=0)
                    # Continue with your processing
                else:
                    return Response({"error": "Failed to load the image"}, status=400)

                # load model
                model = tf.keras.models.load_model(os.getcwd() + '/model-cifar10-v3.h5')
                result = model.predict(test_image) 

                logger.info(result)
                try:
                    os.remove(os.path.join(fss.location, _image))  # Đảm bảo đường dẫn đúng
                except OSError as e:
                    logger.error(f"Error deleting file {_image}: {e.strerror}")
                
                dataset = models.Dataset.objects.filter(slug=dataset).first()
                labels = models.Label.objects.filter(dataset=dataset)

                result_list = result[0].tolist()
              
                label_objects = []
                
                for i in range(len(result_list)):
                    label_object = {
                        'name': labels[i].name,
                        'index': labels[i].index,
                        'accuracy': float(result_list[i])
                    }
                    label_objects.append(label_object)

                logger.info(label_objects)

                # return Response(json.dumps(label_objects))
                return Response(label_objects)
            except MultiValueDictKeyError:
                return Response({"error": "No Image Selected"}, status=400)
        else:
            return Response(serializer.errors, status=400)

class PredictImageCustomTrain(APIView):
    def get(self, request):
        return HttpResponse("test")
    def post(self, request):
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            dataset = serializer.validated_data['dataset']


            fss = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, "tmp"))
            try:
                unique_filename = str(uuid.uuid4()) + ".jpg"  # Ví dụ sử dụng UUID
                _image = fss.save(unique_filename, image)
                path = os.path.join(str(settings.MEDIA_ROOT), '\\tmp', unique_filename)
                # image details
                image_url = fss.url(_image)
                # Read the image
                logger.info(os.getcwd() + path)
                imag=cv2.imread(os.getcwd() + path)
                if imag is not None:
                    img_from_ar = Image.fromarray(imag, 'RGB')
                    resized_image = img_from_ar.resize((32, 32))

                    test_image = np.expand_dims(resized_image, axis=0)
                    # Continue with your processing
                else:
                    return Response({"error": "Failed to load the image"}, status=400)

                # load model
                # model = tf.keras.models.load_model(os.getcwd() + '/model-cifar10-v3.h5')
                model = tf.keras.models.load_model(os.path.join(os.getcwd(), 'uploads', dataset, 'model.keras'))
                result = model.predict(test_image) 

                logger.info(result)
                json_predictions = json.dumps(result.tolist())  
                return HttpResponse(json_predictions, status=200)
                
                try:
                    os.remove(os.path.join(fss.location, _image))  # Đảm bảo đường dẫn đúng
                except OSError as e:
                    logger.error(f"Error deleting file {_image}: {e.strerror}")
                
                dataset = models.Dataset.objects.filter(slug=dataset).first()
                labels = models.Label.objects.filter(dataset=dataset)

                result_list = result[0].tolist()
              
                label_objects = []
                
                for i in range(len(result_list)):
                    label_object = {
                        'name': labels[i].name,
                        'index': labels[i].index,
                        'accuracy': float(result_list[i])
                    }
                    label_objects.append(label_object)

                logger.info(label_objects)

                # return Response(json.dumps(label_objects))
                return Response(label_objects)
            except MultiValueDictKeyError:
                return Response({"error": "No Image Selected"}, status=400)
        else:
            return Response(serializer.errors, status=400)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .train_model import train_model_async
from CNN.Building import Traning
@api_view(['POST'])
def start_training(request):
    logger.info(request.data.data)
    return Response({"message": "Training started"})


def customTraining(request):
    return render(request, 'custom-training.html')
import uuid
from django.core.files.storage import default_storage
def train_model(request):
    if request.method == 'POST':

        unique_id = uuid.uuid4().hex

        # Nhận và deserialize dữ liệu JSON
        data_json = request.POST.get('data')
        if not data_json:
            return JsonResponse({'error': 'No data provided'}, status=400)
        data = json.loads(data_json)

        # Xử lý từng item trong dữ liệu
        for item in data:
            label = item.get('label')
            # Tạo thư mục cho label nếu nó không tồn tại
            label_dir_path = os.path.join(settings.MEDIA_ROOT, 'uploads', unique_id, label)
            if not os.path.exists(label_dir_path):
                os.makedirs(label_dir_path)

            # Lưu các ảnh vào thư mục của label
            for file_key in request.FILES:
                if file_key.startswith('images_'):
                    file = request.FILES[file_key]
                    file_path = os.path.join(label_dir_path, file.name)
                    with default_storage.open(file_path, 'wb+') as destination:
                        for chunk in file.chunks():
                            destination.write(chunk)


            # ce1bd24590af4e73838dc49710f36a6a 
            Traning(unique_id).testing()
            # test1 = Traning('ce1bd24590af4e73838dc49710f36a6a')
            # test1.testing('C://Users//chris//OneDrive//Desktop//detector_python//uploads//ce1bd24590af4e73838dc49710f36a6a')

        return JsonResponse({'message': 'Files uploaded successfully','uuid': unique_id})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
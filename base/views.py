from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse
from . import models
import numpy as np
import logging
import cv2
from CNN.Training import Training
import shutil
import json
import os
from PIL import Image
import uuid
import tensorflow as tf
from django.conf import settings
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ImageSerializer
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
import uuid
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .train_model import train_model_async
# from CNN.Building import Traning
from CNN import Setting
from CNN.Train2 import Building
import base64
import zipfile
def home(request):
    return render(request, 'home.html')

def getting_started(request):
    return render(request, 'getting_started.html')

def train(request):
    return render(request, 'train.html') 

logger = logging.getLogger('django')

def standardTrainingDetail(request, slug):
    sizes = int(request.GET.get('sizes', 10))
    dataset = models.Dataset.objects.filter(slug=slug).first()
    labels = models.Label.objects.filter(dataset=dataset)
    images_by_labels = []
    for label in labels:
        images = models.Image.objects.filter(label=label)[:sizes]
        images_by_labels.append((label, images))
    labels_name = list([label.name for label in labels])
    return render(request, 'standard_training.html', {'images_by_labels': images_by_labels,'dataset': dataset, 'labels': labels_name})

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

@api_view(['POST'])
def start_training(request):
    logger.info(request.data.data)
    return Response({"message": "Training started"})


def customTraining(request):
    labels = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips'] 
    uuid = request.COOKIES.get('uuid')
    print(uuid)
    if uuid != None:    
        labels = os.listdir(os.path.join(settings.MEDIA_ROOT,'static', 'uploads', uuid))

    return render(request, 'custom-training.html', {'labels':labels})



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
            # Traning(unique_id).testing()
            # test1 = Traning('ce1bd24590af4e73838dc49710f36a6a')
            # test1.testing('C://Users//chris//OneDrive//Desktop//detector_python//uploads//ce1bd24590af4e73838dc49710f36a6a')

        return JsonResponse({'message': 'Files uploaded successfully','uuid': unique_id})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def standard_train_model(request):
    if request.method == 'POST':
        dataset = request.POST.get('dataset')
        setting = json.loads(request.POST.get('setting'))
        setting_instance = Setting(
            padding=int(setting.get('padding', 0)),
            epochs=int(setting.get('epochs', 10)),
            patch_sizes=int(setting.get('patch_sizes', 32)),
            stride=int(setting.get('stride', 0)),
            optimizer=setting.get('optimizer', 'adam'),
            loss=setting.get('loss', 'categorical_crossentropy'),
            activation=setting.get('activation', 'softmax'),
            max_pooling=int(setting.get('max_pooling2d', 2))
        )
        logger.info(setting_instance)
        # unique_id = uuid.uuid4().hex
        unique_id = 'f0ace91f3ea44acdb7ab17196a376f17'
        
        folder_dataset = os.path.join(PROJECT_PATH, 'static', 'datasets', 'cifar-10')
        folder = os.path.join(PROJECT_PATH, 'static', 'uploads', unique_id)
        # os.makedirs(folder, exist_ok=True)
        # shutil.copytree(folder_dataset, folder)

        # flower_classifier = Training(10)
        # flower_classifier.build_model()
        # train_generator, validation_generator = flower_classifier.make_data(folder_dataset)
        # flower_classifier.train_model(train_generator, validation_generator)
        # flower_classifier.save_model(folder)

        return HttpResponse({'adsfafasdfds'})
PROJECT_PATH = os.path.abspath(os.path.dirname(__name__))
def train_model2(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        data = body['trainingData']
        setting = body['setting']

        poolingType=setting.get('pooling', 'AveragePooling')
        epochs=int(setting.get('epochs', 20))
        patch_sizes=int(setting.get('patch_sizes', 64))
        test_size=float(setting.get('test_size', 0.2))
        optimizer=setting.get('optimizer', 'adam')
        # setting_instance = Setting(
        #     padding=int(setting.get('padding', 0)),
        #     epochs=int(setting.get('epochs', 10)),
        #     patch_sizes=int(setting.get('patch_sizes', 32)),
        #     stride=int(setting.get('stride', 0)),
        #     optimizer=setting.get('optimizer', 'adam'),
        #     loss=setting.get('loss', 'categorical_crossentropy'),
        #     activation=setting.get('activation', 'softmax'),
        #     max_pooling=int(setting.get('max_pooling2d', 2)),
        #     test_size=int(setting.get('test_size', 0.2))
        # )
        new_folder_name = str(uuid.uuid4())
        new_folder_path = os.path.join(PROJECT_PATH, 'static', 'uploads', new_folder_name)
        # new_folder_path = os.path.join(parent_dir, new_folder_name)
        os.makedirs(new_folder_path)

        for item in data:
            label = item['label']
            images = item['images']
            
            label_folder_path = os.path.join(new_folder_path, label)
            os.makedirs(label_folder_path)
            
            index = 0
            for image_url in images:
                if image_url.startswith('data:image/'):
                    image_data = image_url.split(',')[1]
                    image_binary = base64.b64decode(image_data)
                    new_image_name = f"base64_{index}.jpg"
                    index += 1
                    image_path_destination = os.path.join(label_folder_path, new_image_name)
                    with open(image_path_destination, 'wb') as file:
                        file.write(image_binary)
                else:
                    new_image_name = os.path.basename(image_url)
                    image_path_source = PROJECT_PATH + image_url
                    image_path_destination = os.path.join(label_folder_path, new_image_name)
                    shutil.copy(image_path_source, image_path_destination)

       
        # train_model(new_folder_path)

        # flower_classifier = Training(10, setting_instance)
        # flower_classifier.build_model()
        # train_generator, validation_generator = flower_classifier.make_data(new_folder_path)
        # flower_classifier.train_model(train_generator, validation_generator)
        # flower_classifier.save_model(new_folder_path)

        class_names = [dt['label'] for dt in list(data)]

       
        # img_width = img_height = 32
        num_classes = len(os.listdir(new_folder_path))
        # classifier = Building(new_folder_path, img_height, img_width, num_classes, class_names, epochs,patch_sizes,optimizer,test_size)
        # classifier.build_model()
        # classifier.train2()

        # classifier.evaluate()
        # classifier.save_model()

        # folder = os.path.join(PROJECT_PATH, 'static', 'uploads', '653da5c0-8b41-47ba-ae52-90095c7190bc')
        # setting = Setting(padding=0, epochs=10, patch_sizes=32, stride=0, optimizer='adam', loss='categorical_crossentropy', activation='softmax',max_pooling=2, test_size=0.2, num_classes=num_classes)
        flower_classifier = Training(size=112, epochs=epochs, patch_sizes=patch_sizes,test_size=test_size, optimizer=optimizer,num_classes=num_classes,folder_path = new_folder_path,PoolingType=poolingType)

        # flower_classifier = Training(num_classes)
        flower_classifier.build_model()
        train_generator, validation_generator = flower_classifier.make_data()
        flower_classifier.train_model(train_generator, validation_generator)
        flower_classifier.save_model()


        for folder in class_names:
            subfolder_path = os.path.join(new_folder_path, folder)
            if os.path.isdir(subfolder_path):
                for file_name in os.listdir(subfolder_path):
                    file_path = os.path.join(subfolder_path, file_name)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Không thể xóa {file_path}: {e}")
                os.rmdir(subfolder_path)

        # zip the model
 
        with open(os.path.join(new_folder_path,'label.txt'), 'w') as file:
            for index, class_name in enumerate(class_names):
                file.write(f"{index} {class_name}\n")

        with zipfile.ZipFile(os.path.join(new_folder_path,'tfjs.zip'), 'w') as zipf:
            for root, _, files in os.walk(new_folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Kiểm tra phần mở rộng của file và chỉ zip file có phần mở rộng là .json, .bin, hoặc label.txt
                    if file.endswith('.json') or file.endswith('.bin') or file == 'label.txt':
                        zipf.write(file_path, arcname=os.path.relpath(file_path, new_folder_path))

        # labels = models.Label.objects.filter(dataset= models.Dataset.objects.get(""))

        return JsonResponse({'status': 'success', 'message': 'Model trained successfully', 'uuid': new_folder_name})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


def migarate_data(request):
    PROJECT_PATH = os.path.abspath(os.path.dirname(__name__)) 
    name_dataset = 'flowers'
    folder_dataset = os.path.join(PROJECT_PATH, 'static', 'datasets', name_dataset)

    # class_names = os.listdir(folder_dataset)
    # class_names = ['0','1','2','3','4', '5', '6', '7', '8', '9']
    dataset = models.Dataset.objects.get(slug=name_dataset)
    # class_names = ['Tshirt', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag',
    #                'Ankle boot']
    class_names =  ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']
    # for class_name in class_names:
    #     # Lấy đối tượng nhãn dựa trên tên lớp
    #     label = models.Label.objects.get(name=class_name)
    #
    #     # Lấy tất cả các hình ảnh thuộc nhãn này
    #     images = models.Image.objects.filter(label=label)
    #
    #     # Xóa tất cả các hình ảnh
    #     images.delete()
    # for i, class_name in enumerate(class_names):
    #     label, created = models.Label.objects.get_or_create(name=class_name, index=i, dataset=dataset)

    # Thêm các ảnh vào cơ sở dữ liệu với nhãn từ 0 đến 9
    for class_name in class_names:
        class_dir = os.path.join(folder_dataset, class_name)
        label = models.Label.objects.get(name=class_name)
        image_files = os.listdir(class_dir)
        # for image_file in image_files:
            # Thêm tên ảnh vào cơ sở dữ liệu
            # image_name = os.path.splitext(image_file)[0]
            # print(image_file)
            # models.Image.objects.create(name=image_file, label=label)
            # if image_file.endswith('.png'):
            #     # Tạo tên mới bằng cách thay đổi phần mở rộng từ .png thành .jpg
            #     new_image_file = os.path.splitext(image_file)[0] + '.jpg'
                
            #     # Đường dẫn đến tệp ảnh cũ và mới
            #     old_path = os.path.join(class_dir, image_file)
            #     new_path = os.path.join(class_dir, new_image_file)
            #     # print('old: ' +old_path + ' new: ' + new_path )
            #     # Đổi tên tệp ảnh
            #     os.rename(old_path, new_path)


    return JsonResponse({'message': 'Files uploaded successfully'})



def importModelTraining(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Tạo thư mục mới với UUID
        folder_uuid = str(uuid.uuid4())
        folder_path = os.path.join(PROJECT_PATH, 'static', 'uploads', folder_uuid)
        os.makedirs(folder_path)
        
        # Lưu file zip vào thư mục tạm thời
        with open(os.path.join(folder_path, uploaded_file.name), 'wb') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Giải nén file zip vào thư mục mới
        zip_file_path = os.path.join(folder_path, uploaded_file.name)
        shutil.unpack_archive(zip_file_path, folder_path)
        
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.zip'):
                    file_path = os.path.join(root, file)
                    os.remove(file_path)

        labels = []
        # Mở file label.txt để đọc
        with open(os.path.join(folder_path, 'label.txt'), 'r') as file:
            # Duyệt qua từng dòng trong file
            for line in file:
                # Loại bỏ ký tự index và khoảng trắng ở đầu dòng, sau đó thêm vào danh sách labels
                name = line.split(' ', 1)[1].strip()
                labels.append(name)
        return render(request, 'import-model-training.html', {'uuid': folder_uuid, 'labels': labels})
    return render(request, 'import-model-training.html')

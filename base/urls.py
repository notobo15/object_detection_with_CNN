from django.urls import path, include
from . import views
urlpatterns = [
  # path('', views.home, name ='home'),
  path('', views.getting_started, name ='getting_started'),
  path('train', views.train, name ='train'),
  path('stream', views.stream, name ='tream'),
  path('video', views.video, name ='video'),
  # path('train/standard-training', views.standardTraining, name = 'standardTraining'),
  path('train/standard-training', views.standardTraining, name = 'standardTraining'),
  path('train/standard-training/<slug:slug>', views.standardTrainingDetail, name = 'standardTrainingDetail'),

  path('train/custom-training', views.customTraining, name = 'customTraining'),

   path('predict2', views.PredictImageCustomTrain.as_view(), name='predictCustomTrain'),

   path('predict', views.PredictImageView.as_view(), name='predict_image'),
   path('train-model', views.train_model, name='train-model')
]
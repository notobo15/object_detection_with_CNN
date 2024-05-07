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
  path('train/import-model-training', views.importModelTraining, name = 'importModelTraining'),

   path('predict2', views.PredictImageCustomTrain.as_view(), name='predictCustomTrain'),

   path('predict', views.PredictImageView.as_view(), name='predict_image'),
   path('train-model', views.train_model, name='train-model'),
   path('train-model2', views.train_model2, name='train-model2'),
   path('standard-train-model', views.standard_train_model, name='standard-train-model'),
   path('migrate-data', views.migarate_data, name='migrate-data')
]
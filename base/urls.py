from django.urls import path, include
from . import views
urlpatterns = [
  path('', views.home, name ='home'),
  path('train', views.train, name ='train'),
  # path('train/standard-training', views.standardTraining, name = 'standardTraining'),
  path('train/standard-training', views.standardTrainingDatasets, name = 'standardTrainingDatasets'),
  path('train/standard-training/datasets/<slug:detail>', views.standardTraining, name = 'standardTraining'),
]
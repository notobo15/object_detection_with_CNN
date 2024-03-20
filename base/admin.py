from django.contrib import admin
from .models import Dataset, Label

# Register your models here.

admin.site.register(Dataset)
admin.site.register(Label)
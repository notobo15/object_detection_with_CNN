from django.contrib import admin
from .models import Dataset, Label, Image

# Register your models here.

admin.site.register(Dataset)
admin.site.register(Label)
admin.site.register(Image)
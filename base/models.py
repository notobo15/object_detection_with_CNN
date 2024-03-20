from django.db import models

# Create your models here.
class Dataset(models.Model):
  name = models.CharField(null=True,max_length=100)
  slug = models.SlugField(null=True)
  description = models.TextField(max_length=100)
  img = models.URLField(null=True)
  def __str__(self):
      return f"{self.name}"

class Label(models.Model):
    name = models.CharField(null=True,max_length=100)
    index = models.IntegerField(null=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    img = models.URLField(null=True)
    def __str__(self):
      return f"{self.name}"
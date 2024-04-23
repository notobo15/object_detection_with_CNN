from django.db import models

# Create your models here.
class Dataset(models.Model):
  name = models.CharField(null=True,max_length=100)
  slug = models.SlugField(null=True)
  description = models.TextField(null=True)
  img = models.CharField(null=True,max_length=200)
  def __str__(self):
      return f"{self.name}"

class Label(models.Model):
    name = models.CharField(null=True,max_length=100)
    index = models.IntegerField(null=True)
    dataset = models.ForeignKey(Dataset, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    # img = models.CharField(null=True,max_length=200)
    def __str__(self):
      return f"{self.name}"

class Image(models.Model):
  name = models.CharField(max_length=100, null=True)
  label = models.ForeignKey(Label, on_delete=models.DO_NOTHING)
  def __str__(self):
    return f"{self.name}"
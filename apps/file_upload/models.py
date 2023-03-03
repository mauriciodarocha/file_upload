"""File Upload Model"""
from django.db import models


# Create your models here.
class FileModel(models.Model):
    """File model"""

    doc = models.FileField(upload_to='../../media/')


class MediaFile(models.Model):
    """Media file model"""

    name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    type = models.CharField(max_length=100)

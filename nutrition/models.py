from django.db import models

# Create your models here.
class List(models.Model):
    list_Img = models.ImageField(upload_to='images/')

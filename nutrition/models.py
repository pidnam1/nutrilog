from django.db import models

# Create your models here.
class List(models.Model):
    list_Img = models.ImageField(upload_to='images/')

class Food(models.Model):
    name = models.CharField(max_length=50)
    calories = models.DecimalField(max_digits=6, decimal_places=2)
    carbs = models.DecimalField(max_digits=6, decimal_places=2)
    protein = models.DecimalField(max_digits=6, decimal_places=2)
    fat = models.DecimalField(max_digits=6, decimal_places=2)
    sugar = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
class ListFood(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
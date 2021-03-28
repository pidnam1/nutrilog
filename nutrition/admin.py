from django.contrib import admin

# Register your models here.
from .models import Food, ListFood

admin.site.register(Food)
admin.site.register(ListFood)
from django.contrib import admin

# Register your models here.
from .models import Food, ListFood, List

admin.site.register(Food)
admin.site.register(ListFood)
admin.site.register(List)

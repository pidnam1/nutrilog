from django.urls import path

from . import views

app_name = 'nutrition'
urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('typefile/', views.typefile, name='typefile'),
    path('home/', views.home, name="home")
]
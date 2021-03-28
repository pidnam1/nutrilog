from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'nutrition'
urlpatterns = [
    path('', views.index, name='index'),
    path('success/', views.success, name='success'),
    path('typefile/', views.typefile, name='typefile'),
    path('home/', views.home, name="home")
    path('results/', views.results, name='results'),
    path('googletest/', views.testgoogle, name='testgoogle'),
    path('successfulgoogle/', views.successful_google, name="successful_google")

]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)



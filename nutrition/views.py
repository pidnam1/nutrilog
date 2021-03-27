from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'nutrition/home.html')

def success(request):
    return render(request, 'nutrition/success.html')

def typefile(request):
    return render(request, 'nutrition/typefile.html')

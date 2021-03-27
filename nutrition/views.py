from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from google.cloud import vision
from .forms import *
from .models import Food

def index(request):
    return render(request, 'nutrition/home.html')

def typefile(request):
    return render(request, 'nutrition/typefile.html')

def success(request):
    return render(request, 'nutrition/success.html')
  
def results(request):
    food_list = Food.objects.all()
    

    food_nutrition = {}
    
    for food in food_list:

        #get most likely food from search
        #x_app_id = '31acb5b6'
        #x_app_key = 'b7af62c2e4b293cf1ce74efb6b283935'
        #x_remote_user_id = '0'

        #food_response = requests.get('https://trackapi.nutritionix.com/v2/search/instant?query=%s' % food,
        #    headers={"x-app-id":x_app_id, "x-app-key": x_app_key})
        #json_data_food = json.loads(food_response.text)

        #food_name = json_data_food["common"][0]["food_name"].capitalize()
        #print(food_name)

        #get nutritional info of food
        #nutrition_response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', {"query": food_name},
        #    headers={"x-app-id":x_app_id, "x-app-key": x_app_key})

        #json_data_nutrition = json.loads(nutrition_response.text)

        #calories = json_data_nutrition['foods'][0]['nf_calories']
        #carbs = json_data_nutrition['foods'][0]['nf_total_carbohydrate']
        #protein = json_data_nutrition['foods'][0]['nf_protein']
        #fat = json_data_nutrition['foods'][0]['nf_total_fat']
        #sugar = json_data_nutrition['foods'][0]['nf_sugars']


        food_nutrition[food.name] = {'name': food.name, 'calories':food.calories,
            'carbs': food.carbs, 'protein': food.protein, 'fat': food.fat, 'sugar': food.sugar}
        print(food_nutrition[food.name])
    
    return render(request, 'nutrition/success.html', 
        {'food_nutrition': food_nutrition})

def testgoogle(request):


    if request.method == 'POST':
        form = ListForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('nutrition:successful_google')
    else:
        form = ListForm()
    return render(request, 'nutrition/testgoogle.html', {"form":form})

def successful_google(request):
    lister = List.objects.latest('list_Img')
    list = lister.list_Img
    content = list.read()
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    answers = []
    for text in texts[1:]:
        print('\n"{}"'.format(text.description))
        answers.append("{}".format(text.description))


    return render(request, 'nutrition/successful_google.html', {'list': list, "answers": answers})


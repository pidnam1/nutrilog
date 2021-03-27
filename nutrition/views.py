from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json

def index(request):
    return render(request, 'nutrition/home.html')

def results(request):
    food_list = ['apple', 'orange', 'grapefruit']
    food_nutrition = {}
    
    for food in food_list:

        #get most likely food from search
        x_app_id = '31acb5b6'
        x_app_key = 'b7af62c2e4b293cf1ce74efb6b283935'
        x_remote_user_id = '0'

        food_response = requests.get('https://trackapi.nutritionix.com/v2/search/instant?query=%s' % food, 
            headers={"x-app-id":x_app_id, "x-app-key": x_app_key})
        json_data_food = json.loads(food_response.text)

        food_name = json_data_food["common"][0]["food_name"].capitalize()
        #print(food_name)

        #get nutritional info of food
        nutrition_response = requests.post('https://trackapi.nutritionix.com/v2/natural/nutrients', {"query": food_name}, 
            headers={"x-app-id":x_app_id, "x-app-key": x_app_key})

        json_data_nutrition = json.loads(nutrition_response.text)

        calories = json_data_nutrition['foods'][0]['nf_calories']
        carbs = json_data_nutrition['foods'][0]['nf_total_carbohydrate']
        protein = json_data_nutrition['foods'][0]['nf_protein']
        fat = json_data_nutrition['foods'][0]['nf_total_fat']
        sugar = json_data_nutrition['foods'][0]['nf_sugars']

        food_nutrition[food_name] = {'name': food_name, 'calories':calories, 
            'carbs': carbs, 'protein': protein, 'fat': fat, 'sugar': sugar}
        print(food_nutrition[food_name])
    
    return render(request, 'nutrition/results.html', 
        {'food_nutrition': food_nutrition})

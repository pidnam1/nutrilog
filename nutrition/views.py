from django.http import HttpResponse
from django.shortcuts import render, redirect
import requests
import json
from django.http import JsonResponse
from django.core import serializers
from google.cloud import vision
from .forms import *
from .models import Food, ListFood, List

def index(request):
    return render(request, 'nutrition/home.html')

def indexView(request):
    ListFood.objects.all().delete()
    form = FoodForm()
    foods = ListFood.objects.all()


    return render(request, "nutrition/foodlist.html", {"form": form, "foods": foods})

def postFood(request):
    # request should be ajax and method should be POST.


    if request.is_ajax and request.method == "POST" and 'finished' not in request.POST:
        # get the form data

        form = FoodForm(request.POST)
        # save the data and after fetch the object in instance
        if form.is_valid() and len(ListFood.objects.all()) <= 3:
            instance = form.save()
            # serialize in new friend object in json
            ser_instance = serializers.serialize('json', [ instance, ])
            # send to client side.

            return JsonResponse({"instance": ser_instance}, status=200)
        else:
            # some form errors occured.
            instance = form.save()
            ay = ListFood(name = instance.name)
            ay.save()
            return JsonResponse({"error": ""}, status=400)


    # some error occured
    return JsonResponse({"error": ""}, status=400)

def typefile(request):
    return render(request, 'nutrition/typefile.html')

def home(request):
    return render(request, 'nutrition/home.html')

def success(request):
    
    return render(request, 'nutrition/success.html')
  
def results(request):

    list_food_list = []

    

    food_list = []


    if len(ListFood.objects.all()) > 0:
        list_food_list = ListFood.objects.all()
        for i in list_food_list:
            food_list.append(i.name)
    else:
        
        ##googleapi implementation
        lister = List.objects.last()

        print(List.objects.latest('list_Img'))
        list = lister.list_Img
        content = list.read()
        client = vision.ImageAnnotatorClient()
        image = vision.Image(content=content)

        response = client.text_detection(image=image)
        texts = response.text_annotations
        for text in texts[1:]:
            print('\n"{}"'.format(text.description))
            food_list.append("{}".format(text.description))






    food_nutrition = {}
    print("here ", food_list)
    food_ids = []

    for food in food_list:
        ### Trying to get API Data unless it cant read text
        try:
            data_request = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=4AFvuuDgN33gPTYAYp1bfGSTq7y7sksNFkproiuN&query=%s' % food)
            json_data = json.loads(data_request.text)

        #data_formatted = json.dumps(json_data, indent=4)
        #food_name = json_data['foods'][0]['lowercaseDescription']

            food = json_data['foods'][0]

        
        #data_formatted = json.dumps(food, indent=4)
            food_name = food['lowercaseDescription']
            food_nutrients = food['foodNutrients']
            food_ids.append(food['fdcId'])
        #print(food_ids)
            nutrient_dict = {}
            nutrient_dict["name"] = food_name.capitalize()
            nutrient_dict["score"] = food["score"]
        #print(food['fdcId'])
        #print(food['score'])
            for nutrient in food_nutrients:

                nutrient_id = nutrient['nutrientId']

                if(nutrient['nutrientId'] == 1005):
                    nutrient_dict["carbs"] = [nutrient["value"], nutrient["unitName"].lower()]
                elif(nutrient['nutrientId'] == 1003):
                    nutrient_dict["protein"] = [nutrient["value"], nutrient["unitName"].lower()]
                elif(nutrient['nutrientId'] == 1004):
                    nutrient_dict["fat"] = [nutrient["value"], nutrient["unitName"].lower()]
                elif(nutrient['nutrientId'] == 2000):
                    nutrient_dict["sugar"] = [nutrient["value"], nutrient["unitName"].lower()]
                elif(nutrient['nutrientId'] == 1093):
                    nutrient_dict["sodium"] = [nutrient["value"], nutrient["unitName"].lower()]
            food_nutrition[food_name] = nutrient_dict
        except:
            food_name = "Food not Found"
            food_nutrition[food_name] = "N/A"
    #print(food_nutrition)

    data_request = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=4AFvuuDgN33gPTYAYp1bfGSTq7y7sksNFkproiuN&query=apple')
    json_data = json.loads(data_request.text)
    #json_format = json.dumps(json_data, indent=4)

    #print(json_data)

    
    
    for food in food_list:
        try:
            initial_request = requests.get('https://api.nal.usda.gov/fdc/v1/foods/search?api_key=4AFvuuDgN33gPTYAYp1bfGSTq7y7sksNFkproiuN&query=%s' % food)
            json_data = json.loads(initial_request.text)
            food_id = json_data['foods'][0]['fdcId']
            food_ids.append(food_id)
            print(food_ids)
        except:
            food_ids.append(-1)

    final_recs = []
    for id in food_ids:
        check_ids = int(id)+1
        try:
            data_request = requests.get('https://api.nal.usda.gov/fdc/v1/foods/?fdcIds=%s&api_key=4AFvuuDgN33gPTYAYp1bfGSTq7y7sksNFkproiuN&format=abridged' % check_ids)
            json_data = json.loads(data_request.text)
            #print(json_data[0]['description'])
            
            final_recs.append(json_data[0]['description'])
        except: 
            final_recs.append("Food not found")

    final_recs = final_recs[0:len(final_recs)//2] 
    print(final_recs)
    mylist = zip(food_nutrition.items(), final_recs)
    context = {
        'foods': mylist
    }
    return render(request, 'nutrition/success.html', 
        context)

def testgoogle(request):
    ListFood.objects.all().delete()

    if request.method == 'POST':
        form = ListForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('nutrition:results')
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

def about(request):
    return render(request, 'nutrition/about.html')



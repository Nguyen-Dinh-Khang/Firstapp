from django.shortcuts import render
from .forms import DishAdd, IngredientAdd, DishVegetarianAdd
from .models import Dish, Ingredient, Incompatibility_Ingredient, Dish_Vegetarian
import random
from collections import defaultdict



#DÙNG CHUNG:
def Ingredient_Check_Random(foodlist, random_list, ingredient_mainlist, incompatibility_mainlist, success):
    ingredient_sublist = set()
    incompatibility_sublist = set()
    valid = True
    success[0] = 0
    random_dish = random.choice(foodlist)
    if not random_dish in random_list:       
        if not ingredient_mainlist:
            for ingredient in random_dish.ingredients.all():
                ingredient_mainlist.add(ingredient.ingredient_name)
                for incompatibility in ingredient.incompatible_with.all():
                    incompatibility_mainlist.add(incompatibility.ingredient_name)
            random_list.append(random_dish)
            success[0] = 1
        else: 
            for ingredient in random_dish.ingredients.all():
                if ingredient.ingredient_name in incompatibility_mainlist:
                    valid = False
                    break
                else:
                    ingredient_sublist.add(ingredient.ingredient_name)
                    for incompatibility in ingredient.incompatible_with.all():
                        incompatibility_sublist.add(incompatibility.ingredient_name)
            if valid:
                ingredient_mainlist |= ingredient_sublist
                incompatibility_mainlist |= incompatibility_sublist
                random_list.append(random_dish)
                success[0] = 1


def Ingredient_Check_Add(ingredientlist, ingredient_validlist, ingredient_errorlist, vegetarian_dish):
    incompatibility_list = set()
    incompatibility_path = defaultdict(list)
    for ingredient in ingredientlist:
        name = ingredient.ingredient_name
        if not ingredient_validlist:
            ingredient_validlist.add(name)
            for incompatibility in ingredient.incompatible_with.all():
                incompatibility_list.add(incompatibility.ingredient_name)
                incompatibility_path[name].append(incompatibility.ingredient_name)
        else:
            if name in incompatibility_list:
                for root, ingredients_error in incompatibility_path.items():
                    if name in ingredients_error:
                        ingredient_errorlist[name].add(root)
            else:
                ingredient_validlist.add(name)
                for incompatibility in ingredient.incompatible_with.all():
                    incompatibility_list.add(incompatibility.ingredient_name)
                    incompatibility_path[name].append(incompatibility.ingredient_name)
        if vegetarian_dish[0] == 0 and ingredient.ingredient_category in ['thịt', 'hải sản', 'đồ mặn']:
            vegetarian_dish[0] = 1
    
        
                    





#HOÀN CHỈNH:
def Add_Dish(request):
    dishadd = DishAdd()
    dishvegetarianadd = DishVegetarianAdd()
    if request.method == 'POST':
        dishadd = DishAdd(request.POST)
        dishvegetarianadd = DishVegetarianAdd(request.POST)
        ingredientrawlist = list(request.POST.getlist('ingredient_name'))
        ingredientlist = []
        for name in ingredientrawlist:
            ingredient, _ = Ingredient.objects.get_or_create(ingredient_name = name)
            ingredientlist.append(ingredient)
        ingredient_validlist = set()
        ingredient_errorlist = defaultdict(set)
        vegetarian_dish = [0] 
        Ingredient_Check_Add(ingredientlist, ingredient_validlist, ingredient_errorlist, vegetarian_dish)
        if ingredient_errorlist or not dishadd.is_valid():
            return render(request, 'food_app_pages/food_add.html', {
            'dishadd': dishadd, 
            'ingredientadd': IngredientAdd(),
            'ingredient_values': ingredientrawlist,
            'ingredient_errors': {k: list(v) for k,v in ingredient_errorlist.items()}})
        else:
            dish = dishadd.save()
            for ingredient_name in ingredient_validlist:
                ingredientadd = IngredientAdd(data = {'ingredient_name': ingredient_name})
                if ingredientadd.is_valid():
                    ingredient = ingredientadd.save()
                    dish.ingredients.add(ingredient)
            if dishvegetarianadd.is_valid() and vegetarian_dish[0] == 0:
                dishvegetarian = dishvegetarianadd.save()
                for ingredient_name in ingredient_validlist:
                    ingredientadd = IngredientAdd(data = {'ingredient_name': ingredient_name})
                    if ingredientadd.is_valid():
                        ingredient = ingredientadd.save()
                        dishvegetarian.ingredients.add(ingredient)


    return render(request, 'food_app_pages/food_add.html', {
        'dishadd': DishAdd(), 
        'ingredientadd': IngredientAdd(),
        'ingredient_values': []})


def List_Dish(request):
    context = {"List_dish": Dish.objects.prefetch_related('ingredients')}
    return render(request, 'food_app_pages/food_list.html', context)


def Random_Dish(request):
    random_list = []
    is_vegetarian = None
    ingredient_mainlist = set()
    incompatibility_mainlist = set()
    soup_count = stirfry_count = fried_count = boiled_count = 0

    if request.method == 'POST':
        is_vegetarian = request.POST.get('is_vegetarian')

        if is_vegetarian == '1':
            soup_count = int(request.POST.get('soup_count') or 0)
            if soup_count > 0:
                soup_dish = list(Dish_Vegetarian.objects.filter(dish_vegetarian_category='soup').prefetch_related('ingredients__incompatible_with'))
                soup_count = min(soup_count, len(soup_dish)) 

            stirfry_count =  int(request.POST.get('stirfry_count') or 0)
            if stirfry_count > 0:
                stirfry_dish = list(Dish_Vegetarian.objects.filter(dish_vegetarian_category='stirfry').prefetch_related('ingredients__incompatible_with'))
                stirfry_count = min(stirfry_count, len(stirfry_dish))

            fried_count = int(request.POST.get('fried_count') or 0)
            if fried_count > 0:
                fried_dish = list(Dish_Vegetarian.objects.filter(dish_vegetarian_category='fried').prefetch_related('ingredients__incompatible_with'))
                fried_count = min(fried_count, len(fried_dish)) 

            boiled_count = int(request.POST.get('boiled_count') or 0)
            if boiled_count > 0:
                boiled_dish = list(Dish_Vegetarian.objects.filter(dish_vegetarian_category='boiled').prefetch_related('ingredients__incompatible_with'))
                boiled_count = min(boiled_count, len(boiled_dish))
        else:
            soup_count = int(request.POST.get('soup_count') or 0)
            if soup_count > 0:
                soup_dish = list(Dish.objects.filter(dish_category='soup').prefetch_related('ingredients__incompatible_with'))
                soup_count = min(soup_count, len(soup_dish)) 

            stirfry_count =  int(request.POST.get('stirfry_count') or 0)
            if stirfry_count > 0:
                stirfry_dish = list(Dish.objects.filter(dish_category='stirfry').prefetch_related('ingredients__incompatible_with'))
                stirfry_count = min(stirfry_count, len(stirfry_dish))

            fried_count = int(request.POST.get('fried_count') or 0)
            if fried_count > 0:
                fried_dish = list(Dish.objects.filter(dish_category='fried').prefetch_related('ingredients__incompatible_with'))
                fried_count = min(fried_count, len(fried_dish)) 

            boiled_count = int(request.POST.get('boiled_count') or 0)
            if boiled_count > 0:
                boiled_dish = list(Dish.objects.filter(dish_category='boiled').prefetch_related('ingredients__incompatible_with'))
                boiled_count = min(boiled_count, len(boiled_dish))
            

        
        attempt = 0
        success = [0]
        soup_attempt = 0
        stirfry_attempt = 0
        fried_attempt = 0
        boiled_attempt = 0
        while len(random_list) < (soup_count + stirfry_count + fried_count + boiled_count) and attempt < 50:
            attempt += 1
            if soup_attempt < soup_count:
                Ingredient_Check_Random(soup_dish, random_list, ingredient_mainlist, incompatibility_mainlist, success)
                if success[0] == 1:
                    soup_attempt += 1
            if stirfry_attempt < stirfry_count:
                Ingredient_Check_Random(stirfry_dish, random_list, ingredient_mainlist, incompatibility_mainlist, success)
                if success[0] == 1:
                    stirfry_attempt += 1
            if fried_attempt < fried_count:
                Ingredient_Check_Random(fried_dish, random_list, ingredient_mainlist, incompatibility_mainlist, success)
                if success[0] == 1:
                    fried_attempt += 1
            if boiled_attempt < boiled_count:
                Ingredient_Check_Random(boiled_dish, random_list, ingredient_mainlist, incompatibility_mainlist, success)
                if success[0] == 1:
                    boiled_attempt += 1

    random_list_soup = []
    random_list_stirfry = []
    random_list_fried = []
    random_list_boiled = []
    if is_vegetarian == '1':
        for dish in random_list:
            if dish.dish_vegetarian_category == 'soup':
                random_list_soup.append(dish)
            elif dish.dish_vegetarian_category == 'stirfry':
                random_list_stirfry.append(dish)
            elif dish.dish_vegetarian_category == 'fried':
                random_list_fried.append(dish)
            elif dish.dish_vegetarian_category == 'boiled':
                random_list_boiled.append(dish)
    else:
        for dish in random_list:
            if dish.dish_category == 'soup':
                random_list_soup.append(dish)
            elif dish.dish_category == 'stirfry':
                random_list_stirfry.append(dish)
            elif dish.dish_category == 'fried':
                random_list_fried.append(dish)
            elif dish.dish_category == 'boiled':
                random_list_boiled.append(dish)

    context = {
        "grouped_random": {
            'món canh:': random_list_soup,
            'món xào-kho:': random_list_stirfry,
            'món chiên:': random_list_fried,
            'món luộc-hấp:': random_list_boiled,
        },
        'is_vegetarian': is_vegetarian,
        'ingredients': ingredient_mainlist, 
        'soup_count': soup_count,
        'stirfry_count': stirfry_count,
        'fried_count': fried_count,
        'boiled_count': boiled_count,
    }
    return render(request, 'food_app_pages/food_random.html', context)




#TEST
def Test(request):
    return render(request, 'food_app_pages/foodapp_base2.html')



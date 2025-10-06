from django.contrib import admin
from .models import Dish, Dish_Vegetarian,Ingredient, Incompatibility_Ingredient, Category_Ingredient



class Dish_IngredientInline(admin.TabularInline):
    model = Dish.ingredients.through
    extra = 1
    autocomplete_fields = ['ingredient']



class DishVegetarian_IngredientInline(admin.TabularInline):
    model = Dish_Vegetarian.ingredients.through
    extra = 1
    autocomplete_fields = ['ingredient']



class CategoryIngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1



class IncompatibilityInline(admin.TabularInline):
    model = Incompatibility_Ingredient
    fk_name = 'ingredient1'
    extra = 1



@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('dish_name','ingredient_count')
    search_fields = ('dish_name','dish_category')
    inlines = [Dish_IngredientInline]
    exclude = ('ingredients',)

    def ingredient_count(self, obj):
        return obj.ingredients.count()



@admin.register(Dish_Vegetarian)
class DishVegetarianAdmin(admin.ModelAdmin):
    list_display = ('dish_vegetarian_name', 'ingredient_count')
    search_fields = ('dish_vegetarian_name', 'dish_vegetarian_category')
    inlines = [DishVegetarian_IngredientInline]
    exclude = ('ingredients',)

    def ingredient_count(self, obj):
        return obj.ingredients.count()



@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient_name',)
    search_fields = ('ingredient_name',)
    inlines = [IncompatibilityInline]
    exclude = ('incompatible_with',)



@admin.register(Incompatibility_Ingredient)
class IncompatibilityAdmin(admin.ModelAdmin):
    list_display = ('ingredient1', 'ingredient2', 'get_severity')
    list_filter = ('severity',)
    search_fields = ('ingredient1__ingredient_name', 'ingredient2__ingredient_name')

    def get_severity(self, obj):
        return obj.get_severity_display()



@admin.register(Category_Ingredient)
class CategoryIngredientAdmin(admin.ModelAdmin):
    list_display = ('category_name',)
    list_filter = ('category_name',)
    inlines = [CategoryIngredientInline]



from django import forms
import re
from .models import Ingredient, Dish, Incompatibility_Ingredient, Dish_Vegetarian




class DishAdd(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['dish_name','dish_category']
        labels = {'dish_name': 'Dish name', 'dish_category': 'Dish category'}
        widgets = {
            'dish_name': forms.TextInput(attrs={
                'placeholder': 'Nhập tên món ăn', 
                'class': 'form-control', 
                'autofocus': True}),
            'dish_category': forms.Select(attrs={
                'placeholder':'Chọn loại món ăn',
                'class': 'form-select'})
            }
    

    def clean_dish_name(self):
        dish_name = self.cleaned_data.get('dish_name')
        if not re.fullmatch(r'^[\w\s]+$', dish_name):
            raise forms.ValidationError('Tên món ăn chỉ được chứa chữ cái, chữ số và dấu "_"')
        if Dish.objects.filter(dish_name=dish_name).exists():
            raise forms.ValidationError('Món ăn đã có')
        return dish_name




class DishVegetarianAdd(forms.Form):
    dish_name = forms.CharField(
        max_length= 100,
        label= 'Dish name',
        widget= forms.TextInput(attrs={
            'placeholder': 'Nhập tên món ăn',
            'class': 'form-control',
            'autofocus': True }))
    dish_category = forms.ChoiceField(
        choices= [
            ('soup', 'món canh'),
            ('stirfry', 'món xào (kho)'),
            ('fried', 'món chiên'),
            ('boiled', 'món luộc (hấp)'),
        ],
        label= 'loại món ăn',
        widget= forms.Select(attrs={
            'placeholder': 'Chọn loại món ăn',
            'class': 'form-select'
        })
    )

    def clean_dish_name(self):
        dish_vegetarian_name = self.cleaned_data.get('dish_name')
        if not re.fullmatch(r'^[\w\s]+$', dish_vegetarian_name):
            raise forms.ValidationError('Tên món ăn chỉ được chứa chữ cái, chữ số và dấu "_"')
        if Dish_Vegetarian.objects.filter(dish_vegetarian_name = dish_vegetarian_name).exists():
            raise forms.ValidationError('Món chay đã có')
        return dish_vegetarian_name
    
    def save(self):
        dish = Dish_Vegetarian.objects.create(
            dish_vegetarian_name = self.cleaned_data.get('dish_name'),
            dish_vegetarian_category = self.cleaned_data.get('dish_category')
        )
        return dish




class IngredientAdd(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['ingredient_name']
        labels = {'ingredient_name': 'Ingredient name'}
        widgets = {'ingredient_name': forms.TextInput(attrs={
            'placeholder': 'Nhập nguyên liệu', 
            'class': 'form-control', 
            'autofocus': True})}
    

    def clean_ingredient_name(self):
        ingredient_name= self.cleaned_data.get('ingredient_name')
        if not re.fullmatch(r'^[\w\s]+$', ingredient_name):
            raise forms.ValidationError('Tên nguyên liệu chỉ được chứa chữ cái, chữ số và dấu "_"')
        return ingredient_name
    
    def save(self, commit=True, *args, **kwargs):
        ingredient_name = self.cleaned_data.get('ingredient_name')
        ingredient, _ = Ingredient.objects.get_or_create(ingredient_name=ingredient_name)
        return ingredient
        
    
    







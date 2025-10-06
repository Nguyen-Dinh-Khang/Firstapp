from django.db import models




class Dish(models.Model):
    dish_category = [
        ('soup', 'món canh'),
        ('stirfry', 'món xào (kho)'),
        ('fried', 'món chiên'),
        ('boiled', 'món luộc (hấp)'),   
    ]
    dish_name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField('Ingredient')
    dish_category = models.CharField(choices = dish_category)

    def __str__(self):
        return self.dish_name
    
    class Meta:
        verbose_name = 'Dish'
        verbose_name_plural = 'Dish'



class Dish_Vegetarian(models.Model):
    dish_category = [
        ('soup', 'món canh'),
        ('stirfry', 'món xào (kho)'),
        ('fried', 'món chiên'),
        ('boiled', 'món luộc (hấp)'),
    ]
    dish_vegetarian_name = models.CharField(max_length=100)
    ingredients = models.ManyToManyField('Ingredient')
    dish_vegetarian_category = models.CharField(choices = dish_category)

    def __str__(self):
        return self.dish_vegetarian_name
    
    class Meta:
        verbose_name = 'Vegetarian dish'
        verbose_name_plural = 'Vegetarian dish'



class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=100)
    incompatible_with = models.ManyToManyField(
        'self',
        through='Incompatibility_Ingredient', 
        symmetrical=True, 
        blank=True)   
    ingredient_category = models.ForeignKey(
        'Category_Ingredient',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ingredients")

    def __str__(self):
        return self.ingredient_name

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredient'
    


class Category_Ingredient(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = 'Ingredient category'
        verbose_name_plural = 'Ingredient category'



class Incompatibility_Ingredient(models.Model):
    ingredient1 = models.ForeignKey(Ingredient, related_name='incompatibility_ingredient1', on_delete=models.CASCADE)
    ingredient2 = models.ForeignKey(Ingredient, related_name='incompatibility_ingredient2', on_delete=models.CASCADE)
    SEVERITY_CHOICES = [
        (1, "Nhẹ"),
        (2, "Vừa"),
        (3, "Nặng"),
    ]
    severity = models.IntegerField(choices=SEVERITY_CHOICES)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("ingredient1", "ingredient2")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not Incompatibility_Ingredient.objects.filter(
            ingredient1 = self.ingredient2,
            ingredient2 = self.ingredient1
        ).exists():
            Incompatibility_Ingredient.objects.create(
                ingredient1 = self.ingredient2,
                ingredient2 = self.ingredient1,
                severity = self.severity,
                description = self.description
            )
    
    def __str__ (self):
        return f"{self.ingredient1} kị với {self.ingredient2} mức độ {self.get_severity_display()}"
    
    class Meta:
        verbose_name = 'Ingredient incompatibility'
        verbose_name_plural = 'Ingredient incompatibility'





    


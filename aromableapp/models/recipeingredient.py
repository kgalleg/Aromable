from django.db import models
from .recipe import Recipe
from .ingredient import Ingredient

class RecipeIngredient(models.Model):


    quantity = models.IntegerField(blank=True, null=True)

#foreign keys
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredient_list')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)


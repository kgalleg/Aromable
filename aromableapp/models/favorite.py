from django.db import models
from .recipe import Recipe
from django.urls import reverse

class Favorite(models.Model):

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)


    class Meta:
            verbose_name = ("favorite")
            verbose_name_plural = ("favorites")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("favorite_detail", kwargs={"pk": self.pk})

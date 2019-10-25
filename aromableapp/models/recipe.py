from django.db import models
from .category import Category
from django.urls import reverse
from django.contrib.auth.models import User

class Recipe(models.Model):

    name = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=150, blank=True, null=True)

    #foreign keys
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("recipe")
        verbose_name_plural = ("recipes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("recipe_detail", kwargs={"pk": self.pk})
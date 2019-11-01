from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Ingredient(models.Model):

    name = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=150, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = ("ingredient")
        verbose_name_plural = ("ingredients")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ingredient_detail", kwargs={"pk": self.pk})


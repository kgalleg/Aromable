from django.db import models
from django.urls import reverse

class Ingredient(models.Model):

    name = models.CharField(max_length=50, blank=True, null=True)
    notes = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = ("ingredient")
        verbose_name_plural = ("ingredients")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ingredient_detail", kwargs={"pk": self.pk})


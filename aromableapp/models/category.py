from django.db import models
from django.urls import reverse

class Category(models.Model):

    name = models.CharField(max_length=50)


    class Meta:
        verbose_name = ("category")
        verbose_name_plural = ("categories")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})

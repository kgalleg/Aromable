from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):

    name = models.CharField(max_length=50)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = ("category")
        verbose_name_plural = ("categories")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})

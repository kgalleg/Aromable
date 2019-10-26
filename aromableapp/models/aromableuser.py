from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Aromableuser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)


    class Meta:
        verbose_name = ("Aromableuser")
        verbose_name_plural = ("Aromableusers")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

@receiver(post_save, sender=User)
def create_aromableuser(sender, instance, created, **kwargs):
    if created:
        Aromableuser.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_aromableuser(sender, instance, **kwargs):
    instance.aromableuser.save()
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def CreateProfile(sender, instance, created, **kwargs):
    if created:
        newpro = Profile(user=instance)
        newpro.save()
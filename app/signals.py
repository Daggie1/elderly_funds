from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

from django.dispatch import Signal

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


filemanager_pre_upload = Signal(providing_args=["filename", "path", "filepath"])
filemanager_post_upload = Signal(providing_args=["filename", "path", "filepath"])

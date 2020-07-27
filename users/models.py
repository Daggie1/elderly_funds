import os
from datetime import datetime
from enum import Enum
from django.contrib.contenttypes.models import ContentType
from django.db import models

from django.utils import timezone
from django_fsm import FSMField, transition
from django.contrib.auth.models import User, Permission
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_no = models.CharField(null=True, max_length=25)
    phone = models.CharField(null=True, max_length=25)
    full_name = models.CharField(null=True, max_length=25)
    elderly = models.ForeignKey(User,null=True,on_delete=models.CASCADE, related_name='elderly')
    first_login = models.BooleanField(default=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)



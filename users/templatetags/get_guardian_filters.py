from django import template
from django.contrib.auth.models import User
from users.models import Profile
import urllib

register = template.Library()


@register.filter
def get_guardian(user_id):
    related_profile= Profile.objects.get(elderly_id=user_id)

    return  User.objects.get(profile__elderly_id=int(user_id))
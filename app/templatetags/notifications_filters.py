from django import template
from app.models import Notification
import urllib

register = template.Library()


@register.filter
def unread_notification_count(all_notifications=Notification.objects.none()):


    print(all_notifications)
    all_notifications=all_notifications.filter(read_at=None)
    return all_notifications.count()
@register.filter
def unread_notification_list(all_notifications=Notification.objects.none()):


    print(all_notifications)
    all_notifications.filter(read_at=None)
    return all_notifications

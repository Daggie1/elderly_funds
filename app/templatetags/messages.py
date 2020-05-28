from django import template
from app.models import Notification

register = template.Library()


@register.filter
def pending_tickets(all_messages=Notification.objects.filter(resolved=False)):
    print(all_messages.count())
    return all_messages.count()

from django import template
from django.forms.widgets import RadioSelect
from notifications.models import Notification

register = template.Library()

@register.filter
def get_digit(dictionary, key):
    return dictionary.get(str(key))[0]

@register.filter
def get_duration(dictionary, key):
    return dictionary.get(str(key))[1]

@register.filter
def is_radio(field):
    return isinstance(field.field.widget, RadioSelect)

@register.filter
def unread_notifications_count(user):
    """
    Returns the count of unread notifications for a given user.
    """
    if user.is_authenticated:
        return Notification.objects.filter(user=user, status=Notification.UNREAD).count()
    return 0

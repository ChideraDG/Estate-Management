from django import template
from django.forms.widgets import RadioSelect

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

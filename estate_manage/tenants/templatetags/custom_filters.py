from django import template

register = template.Library()

@register.filter
def get_digit(dictionary, key):
    return dictionary.get(str(key))[0]

@register.filter
def get_duration(dictionary, key):
    return dictionary.get(str(key))[1]

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, None)

@register.filter
def dict_items(dictionary):
    return dictionary.items()

from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary.get(key)
    return None

@register.filter
def dict_items(dictionary):
    return dictionary.items()

@register.simple_tag
def grade_lookup(dictionary, student_id, date):
    return dictionary.get((student_id, date), '')


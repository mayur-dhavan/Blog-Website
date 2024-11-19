from django import template

register = template.Library()

@register.filter
def get_range_to(value, end_value):
    try:
        return range(value, end_value)
    except TypeError:
        return range(0)

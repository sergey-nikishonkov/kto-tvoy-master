from django import template

register = template.Library()

@register.filter()
def range_f(val):
    return range(val)

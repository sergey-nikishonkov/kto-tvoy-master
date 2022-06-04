from django import template

register = template.Library()


@register.filter()
def get_time(obj):
    return [i.hour for i in obj]


@register.filter()
def is_booked(obj):
    return [i for i in obj if i.booked]


@register.filter()
def is_checked(obj):
    return [i for i in obj if not i.booked]

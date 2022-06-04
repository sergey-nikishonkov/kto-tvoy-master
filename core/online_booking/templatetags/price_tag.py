from django import template
from online_booking.models import Services

register = template.Library()


@register.inclusion_tag('online_booking/price.html')
def get_servises():
    """Show services at the home page"""
    services = Services.objects.filter(show_on_main_page=True)
    return {'services': services}



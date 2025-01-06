from django import template

register = template.Library()


@register.filter
def format_price(value):
    return f"{value:,}"


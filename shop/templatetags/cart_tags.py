from django import template

register = template.Library()

@register.filter
def price_with_shipping(price: float, shipping: float):
    return round(shipping + price, 2)

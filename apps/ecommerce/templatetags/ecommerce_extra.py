from django import template

register = template.Library()
@register.filter
def prodcost(quantity, price):
    return quantity*price

@register.filter
def totalprice(subtotal, shipping):
    return subtotal+shipping

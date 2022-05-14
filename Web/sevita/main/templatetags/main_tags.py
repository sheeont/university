from django import template
from main.models import *

register = template.Library()


@register.simple_tag()
def get_products():
    return Product.objects.all()


@register.filter(name='cut')
def cut(products, count):
    if count:
        db_amount = products.count()
        if db_amount >= count:
            products = products.filter(pk__gte=db_amount - count)

    return products


register.filter('cut', cut)

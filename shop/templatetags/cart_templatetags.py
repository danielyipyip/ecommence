from django import template
from shop.models import Order, Item
from django.shortcuts import reverse

register = template.Library()

@register.filter
def cart_item_count(user): 
    if user.is_authenticated:
        querySet=Order.objects.filter(user=user, paid=False)
        if querySet.exists():
            return querySet[0].orderitems.count()
    return 0

@register.filter
def order_count(user):
    if user.groups.exists():
        group=user.groups.all()[0].name #only 1 role for now
        if group in 'shop_admin':
            querySet = Order.objects.filter(complete=False)
            return querySet.count()
    return 0

@register.filter
def similar_items(): 
    #gender, type, season
    querySet = Item.objects.filter()
    # filter(product_season=season, product_type=type)
    print(querySet)
    return querySet

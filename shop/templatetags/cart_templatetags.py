from django import template
from shop.models import Order, Item, Gender_choice, Type_choice, Season_choice, shop_config
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

@register.simple_tag
def gender_categories(): 
    gender_qs = Gender_choice.objects.all()
    return gender_qs

@register.simple_tag
def type_categories(): 
    type_qs = Type_choice.objects.all()
    return type_qs

@register.simple_tag
def season_categories(): 
    season_qs = Season_choice.objects.all()
    return season_qs


@register.simple_tag
def get_shop_links(): 
    links_qs = shop_config.objects.all()[0]
    return links_qs

# @register.filter
# def similar_items(): 
#     #gender, type, season
#     querySet = Item.objects.filter()
#     # filter(product_season=season, product_type=type)
#     print(querySet)
#     return querySet

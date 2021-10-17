from django import template
from shop.models import Order

register = template.Library()

@register.filter
def cart_item_count(user): 
    if user.is_authenticated:
        querySet=Order.objects.filter(user=user, paid=False)
        if querySet.exists():
            return querySet[0].orderitems.count()
    return 0

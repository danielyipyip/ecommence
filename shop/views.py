from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from shop.models import Item, Order, OrderItem

# Create your views here.
class homePage(ListView):
    model = Item
    paginate_by=2
    template_name='home.html'

class productDetailPage(DetailView):
    model=Item
    template_name="product_detail.html"

def add_to_cart(request, pk):
    #get/create item, order, order_item
    item=get_object_or_404(Item, pk=pk)
    order=Order.objects.get_or_create(user=request.user, paid=False)
    #need extra variable since cannot access .orderitems field directly?
    current_order=order[0]
    orderItem, create_orderItem=OrderItem.objects.get_or_create(item=item, user=request.user, paid=False)
    if create_orderItem:
        current_order.orderitems.add(orderItem)
    else:
        orderItem.quantity+=1
        #need save
        orderItem.save()
    return redirect("shop:home-page")

def remove_from_cart(request, pk):
    #get/create item, order, order_item
    item=get_object_or_404(Item, pk=pk)
    order=Order.objects.filter(user=request.user, paid=False)
    if order.exists():
        current_order=order[0]
        if OrderItem.objects.filter(item=item, user=request.user, paid=False).exists():
            orderItem=OrderItem.objects.filter(item=item, user=request.user, paid=False)[0]
            current_order.orderitems.remove(orderItem)
            orderItem.delete()
        else:
            #no item
            pass
    else:
        #no order
        pass
    return redirect("shop:home-page")


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
    orderItem, create_orderItem=OrderItem.objects.get_or_create(item=item, user=request.user, paid=False)
    if create_orderItem:
        order.orderitems.add(orderItem)
    else:
        orderItem.quantity+=1
    #order.save()
    return redirect("shop:home-page")

def remove_from_cart(request, pk):
    #get/create item, order, order_item
    item=get_object_or_404(Item, pk=pk)
    order=Order.objects.get_or_create(user=request.user, paid=False)
    orderItem, create_orderItem=OrderItem.objects.get_or_create(item=item, user=request.user, paid=False)
    if create_orderItem:
        order.orderitems.add(orderItem)
    else:
        orderItem.quantity+=1
    order.save()
    return redirect("shop:home-page")

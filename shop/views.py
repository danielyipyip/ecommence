from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from shop.models import Item, Order, OrderItem, Address
from.forms import CheckoutForm

from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect

# Create your views here.
class homePage(ListView):
    model = Item
    paginate_by=2
    template_name='home.html'

class productDetailPage(DetailView):
    model=Item
    template_name="product_detail.html"

#does 2 things: (1)add to cart (2)quantity+1
#@login_required
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
    #return redirect("shop:home-page")

@login_required
def add_to_cart_product_detail(request, pk):
    add_to_cart(request, pk)
    return redirect("shop:product-detail", pk=pk)

@login_required
def add_to_cart_shopping_cart(request, pk):
    add_to_cart(request, pk)
    return redirect("shop:shopping-cart")



#only does removing item
@login_required
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

def remove_from_cart_shopping_cart(request,pk):
    remove_from_cart(request, pk)
    return redirect("shop:shopping-cart")

#quantity -1
@login_required
def quantity_reduce(request, pk):
    #get/create item, order, order_item
    item=get_object_or_404(Item, pk=pk)
    order=Order.objects.filter(user=request.user, paid=False)
    if order.exists():
        current_order=order[0]
        if OrderItem.objects.filter(item=item, user=request.user, paid=False).exists():
            orderItem=OrderItem.objects.filter(item=item, user=request.user, paid=False)[0]
            if orderItem.quantity==1:
                current_order.orderitems.remove(orderItem)
                orderItem.delete()
                messages.info(request, "This item is removed")
            else:
                orderItem.quantity-=1
                #need save
                orderItem.save()
        else:
            #no item
            pass
    else:
        #no order
        pass
    
def quantity_reduce_shopping_cart(request,pk):
    quantity_reduce(request, pk)
    return redirect("shop:shopping-cart")
    
class shoppingCart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order=Order.objects.get(user=self.request.user, paid=False)
        context={'object': order}
        return render(self.request, 'shopping_cart.html', context)

class checkout_view(View):
    def get(self, *args, **kwargs):
        form=CheckoutForm()
        context={'form': form}
        return render(self.request, 'checkout.html', context)
    def post(self, *args, **kwargs):
        form=CheckoutForm(self.request.POST or None)
        try: 
            order=Order.objects.get(user=self.request.user, paid=False)
        except ObjectDoesNotExist: 
            messages.info(self.request, "Order not exist")
        if form.is_valid():
            ship_addr1=form.cleaned_data.get('ship_addr1')
            ship_addr2=form.cleaned_data.get('ship_addr2')
            ship_addr3=form.cleaned_data.get('ship_addr3')
            ship_country=form.cleaned_data.get('ship_country')
            ship_zip=form.cleaned_data.get('ship_zip')
            payment_option=form.cleaned_data.get('payment_option')
            ship_addr=Address(user=self.request.user, address_type='s', addr1=ship_addr1, 
            addr2=ship_addr2, addr3=ship_addr3, country=ship_country, zip_code=ship_zip, )
            print(ship_addr)
            ship_addr.save()
            order=Order.objects.get(user=self.request.user, paid=False)
            order.ship_addr=ship_addr
            order.save()
            if payment_option=='C':
                return redirect('shop:checkout')
            elif payment_option=='P':
                return redirect('shop:checkout')
            else:
                return redirect('shop:checkout')

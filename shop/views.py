from typing import Tuple
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from shop.models import Item, Order, OrderItem, Address, UserProfile
from.forms import CheckoutForm, addProductForm

from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect
from .decorators import allowed_users

admin_role_decorator=[login_required, allowed_users(allowed_roles='shop_admin')]

# Create your views here.
def home(request):
    feature_items=Item.objects.filter(label='recom')[:4]
    context={'featured': feature_items, }
    return render(request, "home.html", context)

class homePage(ListView):
    model = Item
    paginate_by=8
    template_name='list_view.html'
    ordering=['name']

class productDetailPage(DetailView):
    model=Item
    template_name="product_detail.html"

class productCategory(ListView):
    model=Item
    paginate_by=8
    template_name='list_view.html'
    def get_queryset(self):
        filter_category=self.kwargs['category']
        if (filter_category in Item.type_name) or (filter_category in Item.type_value):
            item_type = Item.objects.filter(product_type=filter_category)
            return item_type
        elif (filter_category in Item.season_name) or (filter_category in Item.season_value):
            item_season = Item.objects.filter(product_season=filter_category)
            return item_season
        elif (filter_category in Item.label_name) or (filter_category in Item.label_value):
            item_label = Item.objects.filter(label=filter_category)
            return item_label
        else:
            return Item.objects.all()

#does 2 things: (1)add to cart (2)quantity+1
@login_required
def add_to_cart(request, pk):
    #get/create item, order, order_item
    item=get_object_or_404(Item, pk=pk)
    order=Order.objects.get_or_create(user=request.user, paid=False)
    #need extra variable since cannot access .orderitems field directly?
    current_order=order[0]
    #current_order=order #why this NOT ok???
    orderItem, create_orderItem=OrderItem.objects.get_or_create(item=item, user=request.user, paid=False)
    if create_orderItem:
        current_order.orderitems.add(orderItem)
        current_order.save()
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

@login_required
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
    
@login_required
def quantity_reduce_shopping_cart(request,pk):
    quantity_reduce(request, pk)
    return redirect("shop:shopping-cart")
    
class shoppingCart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order=Order.objects.filter(user=self.request.user, paid=False)
        #this line is needed, because order is queryset, [0] assigned is??
        #but still why??? 
        myorder=order[0]
        context={'object': myorder}
        return render(self.request, 'shopping_cart.html', context)

class checkout_view(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form=CheckoutForm()
        order=Order.objects.get(user=self.request.user, paid=False) 
        context={'form': form, 'object':order}
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

class payment_view(LoginRequiredMixin, View):
    def get(self, *args, **kargs):
        order=Order.objects.get(user=self.request.user, paid=False)
        context={'object': order}
        return render(self.request, 'payment.html', context)
    
def payment_sucess(request):
    return render(request, 'payment_sucess.html')

def payment_unsucess(request):
    return render(request, 'payment_unsucess.html')

@method_decorator(admin_role_decorator, name='dispatch')
class itemListView(ListView):
    model = Item
    paginate_by=20
    template_name='itemList_owner.html'
    ordering=['pk']

@method_decorator(admin_role_decorator, name='dispatch')
class update_item_view(DetailView):
    model=Item
    template_name="product_detail.html"

@method_decorator(admin_role_decorator, name='dispatch')
class upload_new_item_view(View):
    def get(self, *args, **kwargs):
        my_pk=self.kwargs.get('pk', None)
        if my_pk:
            form=addProductForm(instance=Item.objects.get(pk=my_pk))
        else:
            form=addProductForm()
        context={'form': form,}
        return render(self.request, 'upload_item.html', context)
    def post(self, *args, **kwargs):
        form=addProductForm(self.request.POST or None)
        new_item=form.save()
        return redirect('shop:item-list')

@method_decorator(admin_role_decorator, name='dispatch')
class OrdersListView(ListView):
    model = Order
    paginate_by=20
    template_name='itemList_owner.html'
    ordering=['pk']
    def get_queryset(self):
        if 'all' in self.kwargs:
            return Order.objects.all
        else:
            order_not_complete = Order.objects.filter(complete=False)
            return order_not_complete
    
def unauthorized_redirect(request):
    return render(request, 'not_authenticated.html')
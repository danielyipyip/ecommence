from typing import Tuple
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from shop.models import Item, Order, OrderItem, Address, homepage_config, navbar_dropdown_config
from.forms import CheckoutForm, addProductForm, homepage_config_form, item_quantity

from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth import authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.shortcuts import redirect
from .decorators import allowed_users
from django.core.mail import send_mail
from django.db.models import Q

admin_role_decorator=[login_required, allowed_users(allowed_roles='shop_admin')]

# Create your views here.
def home(request):
    feature_items=Item.objects.filter(label='recom')[:4]
    home_config = homepage_config.objects.get_or_create()[0]
    context={'featured': feature_items, 'home_config':home_config}
    #print(home_config.banner_image)
    return render(request, "home.html", context)

class homePage(ListView):
    model = Item
    paginate_by=8
    template_name='list_view.html'
    # ordering=['name']
    def get_queryset(self):
        season = self.request.GET.get("season", "")
        gender = self.request.GET.get("gender", "")
        type = self.request.GET.get("type", "")
        order_by = self.request.GET.get("orderby", "pk")
        #(1a)get qs
        item = Item.objects.all()
        #(1b): filter qs by each condition
        if type!="":
            item = item.filter(product_type=type)
        if season!="": 
            item = item.filter(product_season=season)
        if gender!="":
            item = item.filter(product_gender=gender)
        #(1c) sort qs
        item=item.order_by(order_by)
        #(2) return defalt qs
        if type=="" and season=="" and gender=="":
            item=Item.objects.all().order_by(order_by)
        return item
    def get_context_data(self, **kwargs):
        # I think is trying to pass more field in the context var
        context = super(homePage, self).get_context_data(**kwargs)
        context["season"]=self.request.GET.get("season", "")
        context["gender"]=self.request.GET.get("gender", "")
        context["type"]=self.request.GET.get("type", "")
        context["orderby"]=self.request.GET.get("orderby", "")
        context["all_fields"]=Item._meta.get_fields()        
        context["gender_choice"] = Item.gender_choice
        context["season_choice"] = Item.season_choice
        context["type_choice"] = Item.type_choice
        return context

# class productDetailPage(DetailView):
#     model=Item
#     template_name="product_detail.html"

class productDetailPage(View):
    def get(self, *args, **kwargs):
        my_pk=self.kwargs.get('pk', None)
        my_item=Item.objects.filter(pk=my_pk)[0]
        qs=Item.objects.filter(product_type=my_item.product_type, product_season=my_item.product_season)[:3]
        print(qs)
        context={'object':my_item, 'qs': qs}
        # context={'object':my_item,}
        return render(self.request, 'product_detail.html', context)
    
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
def add_to_cart(request, pk, amount=1):
    #get/create item, order, order_item
    item=get_object_or_404(Item, pk=pk)
    order=Order.objects.get_or_create(user=request.user, paid=False)
    #need extra variable since cannot access .orderitems field directly?
    current_order=order[0]
    #current_order=order #why this NOT ok???
    orderItem, create_orderItem=OrderItem.objects.get_or_create(item=item, user=request.user, paid=False)
    if create_orderItem:
        orderItem.quantity=int(amount)
        orderItem.save()
        current_order.orderitems.add(orderItem)
        current_order.save()
    else:
        orderItem.quantity+=int(amount)
        #need save
        orderItem.save()
    #return redirect("shop:home-page")

@login_required
def add_to_cart_product_detail(request, pk):
    if request.method=='POST':
        quantity = request.POST.get('quantity', None)
        print(quantity)
        add_to_cart(request, pk, quantity)
        return redirect("shop:product-detail", pk=pk)
    else:
        return redirect("shop:product-detail", pk=pk)
    

# @login_required
# def add_to_cart_product_detail(request, pk, amount=1):
#     add_to_cart(request, pk, amount)
#     return redirect("shop:product-detail", pk=pk)

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
        #get address
        address=order.ship_addr
        if address: #if there is existing addr (load in form if it does)
            form=CheckoutForm(instance=address)
        context={'form': form, 'object':order}
        return render(self.request, 'checkout.html', context)
    def post(self, *args, **kwargs):
        if Order.objects.get(user=self.request.user, paid=False).ship_addr:
            address=Order.objects.get(user=self.request.user, paid=False).ship_addr
            form=CheckoutForm(self.request.POST, self.request, instance=address or None)
        else:
            form=CheckoutForm(self.request.POST, self.request or None)
        #print(form)
        try: #check does order exist
            order=Order.objects.get(user=self.request.user, paid=False)
        except ObjectDoesNotExist: 
            messages.info(self.request, "Order not exist")
        if form.is_valid():
            ship_addr=form.save()
            print(ship_addr)
            order=Order.objects.get(user=self.request.user, paid=False)
            order.ship_addr=ship_addr
            order.save()
            return redirect('shop:payment')
        else: 
            return redirect('shop:checkout')

class payment_view(LoginRequiredMixin, View):
    def get(self, *args, **kargs):
        order=Order.objects.get(user=self.request.user, paid=False)
        context={'object': order}
        return render(self.request, 'payment.html', context)
    
def payment_sucess(request):
    order=Order.objects.filter(user=request.user, paid=False)[0]
    #turn to paid
    order.paid=True
    order.save()
    #reduce stock
    for order_item in order.orderitems:
        if order_item.item.stock > order_item.quantity:
            order_item.item.stock -= order_item.quantity
        else: 
            pass
            #Not enough error
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
        context={'form': form, 'pk': my_pk}
        return render(self.request, 'upload_item.html', context)
    def post(self, *args, **kwargs):
        #the [0] is needed, from .filter: gives querySet, not just a tuple
        my_pk=self.kwargs.get('pk', None)
        if my_pk:
            curr_item = Item.objects.filter(pk=my_pk)[0]
            if curr_item:
            #need to have self.request.FILE: for the image, otherwise use default image
            #on html side, need enctype='multipart/form-data' so that image files is sent back
                form=addProductForm(self.request.POST, self.request.FILES, instance=curr_item)
        else: 
            form=addProductForm(self.request.POST, self.request.FILES or None)
        if form.is_valid():
            form.save()
        return redirect('shop:item-list')

#only does removing item
@allowed_users(allowed_roles=['shop_admin'])
def remove_item(request, pk):
    #get/create item, order, order_item
    item=get_object_or_404(Item, pk=pk)
    if item:
        item.delete()
    return redirect("shop:item-list")

@method_decorator(admin_role_decorator, name='dispatch')
class OrdersListView(ListView):
    model = Order
    paginate_by=20
    template_name='orderList_owner.html'
    ordering=['pk']
    def get_queryset(self):
        if 'all' in self.kwargs:
            return Order.objects.all
        else:
            order_not_complete = Order.objects.filter(complete=False)
            return order_not_complete
    
def unauthorized_redirect(request):
    return render(request, 'not_authenticated.html')

def search_result(request):
    context={}
    # import os
    # print(os.path.join(settings.MEDIA_DIR,"product_images", "white_tshirt.jpg"))
    if request.method=='POST':
        keyword = request.POST.get('searched', None)
        items=Item.objects.filter(Q(name__contains=keyword) | Q(description__contains=keyword)) 
        context={'keyword': keyword, 'items': items}
        return render(request, 'search_result.html', context)
    else:
        return render(request, 'search_result.html', context)

@method_decorator(admin_role_decorator, name='dispatch')
class modify_homepage_config(View):
    def get(self, *args, **kwargs):
        curr_config=homepage_config.objects.get_or_create()[0]
        form = homepage_config_form(instance=curr_config)
        context={'form': form}
        return render(self.request, 'homepage_config.html', context)
    def post(self, *args, **kwargs):
        curr_config=homepage_config.objects.get_or_create()[0]
        form=homepage_config_form(self.request.POST, self.request.FILES, instance=curr_config)
        print(form)
        if form.is_valid():
            form.save()
        return redirect('shop:home-page')

#thinking how to do
@method_decorator(admin_role_decorator, name='dispatch')
class modify_narbar_config(View):
    def get(self, *args, **kwargs):
        #get all instead
        curr_config=navbar_dropdown_config.objects.filter()


        form = homepage_config_form(instance=curr_config)
        context={'form': form}
        return render(self.request, 'homepage_config.html', context)
    def post(self, *args, **kwargs):
        curr_config=homepage_config.objects.get_or_create()[0]
        form=homepage_config_form(self.request.POST, self.request.FILES, instance=curr_config)
        print(form)
        if form.is_valid():
            form.save()
        return redirect('shop:home-page')

def about_page(request):
    return render(request, 'about_us.html')


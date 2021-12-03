from django.db.models import Q
from django.core.mail import send_mail
from .decorators import allowed_users
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from typing import Tuple
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View

from shop.models import (
    Item, Order, OrderItem, Address, homepage_config, navbar_dropdown_config, Season_choice, Type_choice, 
    Gender_choice, contact_us_config, page_link, shop_config)
from.forms import (CheckoutForm, addProductForm, homepage_config_form, item_quantity, contact_us_config_form, 
page_link_form, season_choice_form, type_choice_form, gender_choice_form, shop_config_form, modify_order_form)
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

admin_role_decorator = [login_required, allowed_users(allowed_roles='shop_admin')]


def home(request):
    feature_items = Item.objects.filter(label='recom')[:4]
    home_config = homepage_config.objects.get_or_create()[0]
    context = {'featured': feature_items, 'home_config': home_config}
    # print(home_config.banner_image)
    return render(request, "home.html", context)

class homePage(ListView):
    model = Item
    # pagination = request.GET.get("pagination", 8)
    # paginate_by = pagination
    paginate_by = 8
    template_name = 'list_view.html'
    # ordering=['name']
    def get_queryset(self):
        season = self.request.GET.get("season", "")
        gender = self.request.GET.get("gender", "")
        type = self.request.GET.get("type", "")
        order_by = self.request.GET.get("orderby", "pk")
        # (1a)get qs
        item = Item.objects.all()
        # (1b): filter qs by each condition
        if type != "":
            item = item.filter(product_type__name=type)
        if season != "":
            item = item.filter(product_season__name=season)
        if gender != "":
            item = item.filter(product_gender__name=gender)
            # item = item.filter(product_gender=gender)
        # (1c) sort qs
        item = item.order_by(order_by)
        # (2) return defalt qs
        if type == "" and season == "" and gender == "":
            item = Item.objects.all().order_by(order_by)
        return item

    def get_context_data(self, **kwargs):
        # I think is trying to pass more field in the context var
        context = super(homePage, self).get_context_data(**kwargs)
        context["season"] = self.request.GET.get("season", "")
        context["gender"] = self.request.GET.get("gender", "")
        context["type"] = self.request.GET.get("type", "")
        context["orderby"] = self.request.GET.get("orderby", "")
        context["all_fields"] = Item._meta.get_fields()
        context["gender_choice"] = Gender_choice.objects.all()
        context["season_choice"] = Season_choice.objects.all()
        context["type_choice"] = Type_choice.objects.all()
        return context

class productDetailPage(View):
    def get(self, *args, **kwargs):
        my_pk = self.kwargs.get('pk', None)
        my_item = Item.objects.filter(pk=my_pk)[0]
        qs = Item.objects.filter(
            product_type=my_item.product_type, product_season=my_item.product_season).exclude(pk=my_pk)[:3]
        context = {'object': my_item, 'qs': qs}
        # context={'object':my_item,}
        return render(self.request, 'product_detail.html', context)

class productCategory(ListView):
    model = Item
    paginate_by = 8
    template_name = 'list_view.html'

    def get_queryset(self):
        filter_category = self.kwargs['category']
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

###########################           shopping cart         #######################################
# does 2 things: (1)add to cart (2)quantity+1
@login_required
def add_to_cart(request, pk, amount=1):
    # get/create item, order, order_item
    item = get_object_or_404(Item, pk=pk)
    order = Order.objects.get_or_create(user=request.user, paid=False)
    # need extra variable since cannot access .orderitems field directly?
    current_order = order[0]
    # current_order=order #why this NOT ok???
    orderItem, create_orderItem = OrderItem.objects.get_or_create(
        item=item, user=request.user, paid=False)
    if create_orderItem:
        orderItem.quantity = int(amount)
        orderItem.save()
        current_order.orderitems.add(orderItem)
        current_order.save()
    else:
        orderItem.quantity += int(amount)
        # need save
        orderItem.save()
    # return redirect("shop:home-page")

@login_required
def add_to_cart_product_detail(request, pk):
    if request.method == 'POST':
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

# only does removing item
@login_required
def remove_from_cart(request, pk):
    # get/create item, order, order_item
    item = get_object_or_404(Item, pk=pk)
    order = Order.objects.filter(user=request.user, paid=False)
    if order.exists():
        current_order = order[0]
        if OrderItem.objects.filter(item=item, user=request.user, paid=False).exists():
            orderItem = OrderItem.objects.filter(
                item=item, user=request.user, paid=False)[0]
            current_order.orderitems.remove(orderItem)
            orderItem.delete()
        else:
            # no item
            pass
    else:
        # no order
        pass
    return redirect("shop:home-page")

@login_required
def remove_from_cart_shopping_cart(request, pk):
    remove_from_cart(request, pk)
    return redirect("shop:shopping-cart")

#quantity -1
@login_required
def quantity_reduce(request, pk):
    # get/create item, order, order_item
    item = get_object_or_404(Item, pk=pk)
    order = Order.objects.filter(user=request.user, paid=False)
    if order.exists():
        current_order = order[0]
        if OrderItem.objects.filter(item=item, user=request.user, paid=False).exists():
            orderItem = OrderItem.objects.filter(
                item=item, user=request.user, paid=False)[0]
            if orderItem.quantity == 1:
                current_order.orderitems.remove(orderItem)
                orderItem.delete()
                messages.info(request, "This item is removed")
            else:
                orderItem.quantity -= 1
                # need save
                orderItem.save()
        else:
            # no item
            pass
    else:
        # no order
        pass

@login_required
def quantity_reduce_shopping_cart(request, pk):
    quantity_reduce(request, pk)
    return redirect("shop:shopping-cart")

class shoppingCart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        order = Order.objects.get_or_create(user=self.request.user, paid=False)
        # order = Order.objects.filter(user=self.request.user, paid=False)
        # this line is needed, because order is queryset, [0] assigned is??
        # but still why???
        myorder = order[0]
        context = {'object': myorder}
        return render(self.request, 'shopping_cart.html', context)

###########################           checkout         #######################################
class checkout_view(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, paid=False)
        # get address
        address = order.ship_addr
        if address:  # if there is existing addr (load in form if it does)
            form = CheckoutForm(instance=address)
        context = {'form': form, 'object': order}
        return render(self.request, 'checkout.html', context)

    def post(self, *args, **kwargs):
        if Order.objects.get(user=self.request.user, paid=False).ship_addr:
            address = Order.objects.get(
                user=self.request.user, paid=False).ship_addr
            form = CheckoutForm(self.request.POST,
                                self.request, instance=address or None)
        else:
            form = CheckoutForm(self.request.POST, self.request or None)
        # print(form)
        try:  # check does order exist
            order = Order.objects.get(user=self.request.user, paid=False)
        except ObjectDoesNotExist:
            messages.info(self.request, "Order not exist")
        if form.is_valid():
            ship_addr = form.save()
            print(ship_addr)
            order = Order.objects.get(user=self.request.user, paid=False)
            order.ship_addr = ship_addr
            order.save()
            return redirect('shop:payment')
        else:
            return redirect('shop:checkout')

class payment_view(LoginRequiredMixin, View):
    def get(self, *args, **kargs):
        order = Order.objects.get(user=self.request.user, paid=False)
        context = {'object': order}
        return render(self.request, 'payment.html', context)

###########################           after payment         #######################################
@login_required
def payment_success(request):
    try:
        order = Order.objects.get(user=request.user, paid=False)
        # turn to paid
        order.paid = True
        order.save()
        # reduce stock
        for order_item in order.orderitems.all():
            #have enough
            order_item.paid=paid=True
            order_item.item.stock -= order_item.quantity
            order_item.save()
            order_item.item.save()
            #if not enough -> need special handle of item
            if order_item.item.stock < order_item.quantity:
                pass 
        # email
        # email_subject='New Order for '+order.user
        # email_message='Order Item: \n'
        # for order_item in order.orderitems:
        #     if order_item.item.stock > order_item.quantity:
        #         order_item.item.stock -= order_item.quantity
        #         email_message+=order_item.item.name +' * '+order_item.quantity+'\n'
        #     else:
        #         pass
        #         # Not enough error
        # email_message+="address: "+order.ship_addr
        # send_mail(email_subject,email_message,'p674dd@gmail.com',['p674dd@gmail.com'],fail_silently=False,)
        return render(request, 'payment_success.html')
    except ObjectDoesNotExist:
        messages.info(request, "Order not exist, paymeny was NOT sucessful")
        return redirect('shop:home-page')

@login_required
def payment_unsuccess(request):
    return render(request, 'payment_unsuccess.html')

###########################           shop owner         #######################################
@method_decorator(admin_role_decorator, name='dispatch')
class itemListView(ListView):
    model = Item
    paginate_by = 20
    template_name = 'itemList_owner.html'
    ordering = ['pk']

@method_decorator(admin_role_decorator, name='dispatch')
class upload_new_item_view(View):
    def get(self, *args, **kwargs):
        my_pk = self.kwargs.get('pk', None)
        if my_pk:
            form = addProductForm(instance=Item.objects.get(pk=my_pk))
        else:
            form = addProductForm()
        context = {'form': form, 'pk': my_pk}
        return render(self.request, 'upload_item.html', context)

    def post(self, *args, **kwargs):
        # the [0] is needed, from .filter: gives querySet, not just a tuple
        my_pk = self.kwargs.get('pk', None)
        if my_pk:
            curr_item = Item.objects.filter(pk=my_pk)[0]
            if curr_item:
                # need to have self.request.FILE: for the image, otherwise use default image
                # on html side, need enctype='multipart/form-data' so that image files is sent back
                form = addProductForm(
                    self.request.POST, self.request.FILES, instance=curr_item)
        else:
            form = addProductForm(
                self.request.POST, self.request.FILES or None)
        if form.is_valid():
            form.save()
        return redirect('shop:item-list')

# only does removing item
@allowed_users(allowed_roles=['shop_admin'])
def remove_item(request, pk):
    # get/create item, order, order_item
    item = get_object_or_404(Item, pk=pk)
    if item:
        item.delete()
    return redirect("shop:item-list")

@method_decorator(admin_role_decorator, name='dispatch')
class OrdersListView(ListView):
    model = Order
    paginate_by = 20
    template_name = 'orderList_owner.html'
    ordering = ['pk']
    def get_queryset(self):
        display_paid = self.request.GET.get("paid", "")
        display_complete = self.request.GET.get("complete", "")
        all_order=Order.objects.all()
        if display_paid=='all':
            myorder=all_order
        else:
            myorder=all_order.filter(paid=True)
        if display_complete:
            myorder=myorder
        else:
            myorder=myorder.filter(complete=False)
        return myorder
    def get_context_data(self, **kwargs):
        context = super(OrdersListView, self).get_context_data(**kwargs)
        context["paid"] = self.request.GET.get("paid", "")
        context["complete"] = self.request.GET.get("complete", "")
        return context

@allowed_users(allowed_roles=['shop_admin'])
def complete_order(request, pk):
    try:
        myorder = Order.objects.get(pk=pk)
        if myorder.complete:
            myorder.complete=False
            messages.info(request, "Order id="+str(pk)+" is now marked as incomplete")
        else:
            myorder.complete=True
            messages.info(request, "Order id="+str(pk)+" is now marked as complete")
        myorder.save()
    except ObjectDoesNotExist:
        messages.info(request, "Order does not exist!")
    return redirect('shop:order-list')

@method_decorator(admin_role_decorator, name='dispatch')
class update_order(View):
    def get(self, *args, **kwargs):
        my_pk = self.kwargs.get('pk', None)
        if my_pk:
            form = modify_order_form(instance=Order.objects.get(pk=my_pk))
        else:
            form = modify_order_form()
        context = {'form': form, 'pk': my_pk}
        return render(self.request, 'update_order.html', context)

    def post(self, *args, **kwargs):
        # the [0] is needed, from .filter: gives querySet, not just a tuple
        my_pk = self.kwargs.get('pk', None)
        if my_pk:
            curr_item = Order.objects.filter(pk=my_pk)[0]
            if curr_item:
                # need to have self.request.FILE: for the image, otherwise use default image
                # on html side, need enctype='multipart/form-data' so that image files is sent back
                form = modify_order_form(
                    self.request.POST, self.request.FILES, instance=curr_item)
        else:
            form = modify_order_form(
                self.request.POST, self.request.FILES or None)
        if form.is_valid():
            form.save()
        return redirect('shop:order-list')

@allowed_users(allowed_roles=['shop_admin'])
def remove_order(request, pk):
    # get/create item, order, order_item
    order = get_object_or_404(Order, pk=pk)
    if order:
        order.delete()
    return redirect("shop:order-list")

def unauthorized_redirect(request):
    return render(request, 'not_authenticated.html')

def search_result(request):
    context = {}
    if request.method == 'POST':
        keyword = request.POST.get('searched', None)
        items = Item.objects.filter(
            Q(name__contains=keyword) | Q(description__contains=keyword))
        context = {'keyword': keyword, 'items': items}
        return render(request, 'search_result.html', context)
    else:
        return render(request, 'search_result.html', context)

###########################           modify pages         #######################################
@method_decorator(admin_role_decorator, name='dispatch')
class modify_homepage_config(View):
    def get(self, *args, **kwargs):
        curr_config = homepage_config.objects.get_or_create()[0]
        form = homepage_config_form(instance=curr_config)
        context = {'form': form}
        return render(self.request, 'homepage_config.html', context)

    def post(self, *args, **kwargs):
        curr_config = homepage_config.objects.get_or_create()[0]
        form = homepage_config_form(
            self.request.POST, self.request.FILES, instance=curr_config)
        if form.is_valid():
            form.save()
        return redirect('shop:config-all')

@method_decorator(admin_role_decorator, name='dispatch')
class modify_shop_config(View):
    def get(self, *args, **kwargs):
        curr_config = shop_config.objects.get_or_create()[0]
        form = shop_config_form(instance=curr_config)
        context = {'form': form}
        print('ok ar0')
        return render(self.request, 'shop_config.html', context)

    def post(self, *args, **kwargs):
        print('ok ar1')
        curr_config = shop_config.objects.get_or_create()[0]
        form = shop_config_form(self.request.POST, self.request.FILES, instance=curr_config)
        print('ok ar2')
        if form.is_valid():
            form.save()
        return redirect('shop:config-all')


# thinking how to do

@method_decorator(admin_role_decorator, name='dispatch')
class modify_contact_us(View):
    def get(self, *args, **kwargs):
        curr_config = contact_us_config.objects.get_or_create()[0]
        form = contact_us_config_form(instance=curr_config)
        context = {'form': form}
        return render(self.request, 'contact_config.html', context)

    def post(self, *args, **kwargs):
        curr_config = contact_us_config.objects.get_or_create()[0]
        form = contact_us_config_form(
            self.request.POST, self.request.FILES, instance=curr_config)
        if form.is_valid():
            form.save()
        return redirect('shop:config-all')


#NOT done
@method_decorator(admin_role_decorator, name='dispatch')
class modify_category(View):
    pass
    def get(self, *args, **kwargs):
        context=self.get_all_context()
        #change form if asking for edit
        season = self.request.GET.get("season", "")
        gender = self.request.GET.get("gender", "")
        type = self.request.GET.get("type", "")
        if type != "":
            curr_type = Type_choice.objects.filter(name=type).first()
            curr_form = type_choice_form(instance=curr_type)
            context['curr_type_form']=curr_form
            context['type_edit']=type
        if season != "":
            curr_season = Season_choice.objects.filter(name=season).first()
            curr_form = season_choice_form(instance=curr_season)
            context['curr_season_form']=curr_form
            context['season_edit']=season
        if gender != "":
            curr_gender = Gender_choice.objects.filter(name=gender).first()
            curr_form = gender_choice_form(instance=curr_gender)
            context['curr_gender_form']=curr_form
            context['gender_edit']=gender

        return render(self.request, 'modify_category.html', context)
    def post(self, *args, **kwargs):
        if 'season' in self.request.POST:
            new_form = season_choice_form(self.request.POST)
        if 'type' in self.request.POST:
            new_form = type_choice_form(self.request.POST)
        if 'gender' in self.request.POST:
            new_form = gender_choice_form(self.request.POST)
        if new_form.is_valid():
            new_form.save()
        context=self.get_all_context()
        return render(self.request, 'modify_category.html', context)
    #helper function
    def get_all_context(self):
        seasons = Season_choice.objects.all()
        types = Type_choice.objects.all()
        genders = Gender_choice.objects.all()
        season_form = season_choice_form()
        type_form = type_choice_form()
        gender_form = gender_choice_form()
        context = {'seasons':seasons, 'types':types, 'genders':genders, 'season_form':season_form, 'type_form':type_form, 'gender_form':gender_form}
        return context

#helper fx for removing category
@allowed_users(allowed_roles=['shop_admin'])
def remove_category(Model, pk):
    category = get_object_or_404(Model, pk=pk)
    if category:
        category.delete()

@allowed_users(allowed_roles=['shop_admin'])
def remove_Season(request, pk):
    remove_category(Season_choice, pk)
    return redirect("shop:category-config")
@allowed_users(allowed_roles=['shop_admin'])
def remove_Type(request, pk):
    remove_category(Type_choice, pk)
    return redirect("shop:category-config")
@allowed_users(allowed_roles=['shop_admin'])
def remove_Gender(request, pk):
    remove_category(Gender_choice, pk)
    return redirect("shop:category-config")

#helper fx for edit category
@allowed_users(allowed_roles=['shop_admin'])
def edit_category(request, Model, Form, pk):
    category = get_object_or_404(Model, pk=pk)
    curr_form = Form(request.POST, instance=category)
    if curr_form.is_valid():
        curr_form.save()

@allowed_users(allowed_roles=['shop_admin'])
def edit_Season(request, pk):
    edit_category(request, Season_choice, season_choice_form, pk)
    return redirect("shop:category-config")
@allowed_users(allowed_roles=['shop_admin'])
def edit_Type(request, pk):
    edit_category(request, Type_choice, type_choice_form, pk)
    return redirect("shop:category-config")
@allowed_users(allowed_roles=['shop_admin'])
def edit_Gender(request, pk):
    edit_category(request, Gender_choice, gender_choice_form, pk)
    return redirect("shop:category-config")

def about_page(request):
    contact_config = contact_us_config.objects.get_or_create()[0]
    context={'contact_us': contact_config}
    return render(request, 'about_us.html', context)


@method_decorator(admin_role_decorator, name='dispatch')
class modify_layout(View):
    def get(self, *args, **kwargs):
        #homepage
        curr_homepage_config = homepage_config.objects.get_or_create()[0]
        form = homepage_config_form(instance=curr_homepage_config)
        #shop links
        curr_shop_link = shop_config.objects.get_or_create()[0]
        link_form = shop_config_form(instance=curr_shop_link)
        #contact us
        contact_config = contact_us_config.objects.get_or_create()[0]
        contact_form = contact_us_config_form(instance=contact_config)
        context = {'homepage_form': form, 'link_form': link_form, 'contact_form': contact_form}
        return render(self.request, 'modify_layout.html', context)


from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from .views import (
    add_to_cart, add_to_cart_product_detail, add_to_cart_shopping_cart, 
    remove_from_cart, quantity_reduce_shopping_cart, remove_from_cart_shopping_cart, 
    homePage, productDetailPage, shoppingCart, checkout_view, 
)

app_name='shop'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', homePage.as_view(), name='home-page'), 
    path('product/<int:pk>', productDetailPage.as_view(), name='product-detail'), 
    path('cart/', shoppingCart.as_view(), name="shopping-cart"), 
    path('checkout/', checkout_view.as_view(), name='checkout'), 

    #path('add_to_cart/<int:pk>', add_to_cart, name="add_to_cart"), 
    path('product/add_to_cart/<int:pk>', add_to_cart_product_detail, name="add_to_cart_product_detail"), 
    path('cart/add_to_cart/<int:pk>', add_to_cart_shopping_cart, name="add_to_cart_shopping_cart"), 

    path('remove_from_cart/<int:pk>', remove_from_cart, name="remove_from_cart"), 
    path('cart/remove_from_cart/<int:pk>', remove_from_cart_shopping_cart, name="remove_from_cart_shopping_cart"), 

    path('cart/quantity_reduce/<int:pk>', quantity_reduce_shopping_cart, name="quantity_reduce_shopping_cart"), 

]
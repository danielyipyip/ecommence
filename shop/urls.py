from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from .views import (
    payment_success, payment_unsuccess, unauthorized_redirect, 
    add_to_cart, add_to_cart_product_detail, add_to_cart_shopping_cart, 
    remove_from_cart, quantity_reduce_shopping_cart, remove_from_cart_shopping_cart, 
    homePage, productDetailPage, shoppingCart, checkout_view, payment_view, productCategory, 
    home, search_result, 
    #owner side
    itemListView, upload_new_item_view, update_item_view, OrdersListView, modify_homepage_config, 
    remove_item, remove_category, 
    #company pages
    about_page, 
)

app_name='shop'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', home, name='home-page'), 
    path('home/', home, name='home-page'), 
    path('items/', homePage.as_view(), name='list-page'), 
    path('product/<int:pk>', productDetailPage.as_view(), name='product-detail'), 
    path('cart/', shoppingCart.as_view(), name="shopping-cart"), 
    path('checkout/', checkout_view.as_view(), name='checkout'), 
    path('payment/', payment_view.as_view(), name='payment'),
    path('payment/success/', payment_success, name="payment-success"), 
    path('payment/unsucess/', payment_unsuccess, name="payment-unsuccess"), 
    path('category/<str:category>/', productCategory.as_view(), name="item-by-category"), 
    path('unauthorized/', unauthorized_redirect, name='unauthorized'), 
    path('search/', search_result, name='search'), 
    
    #company pages
    path('about_us/', about_page, name='about-us'), 

    #path('add_to_cart/<int:pk>', add_to_cart, name="add_to_cart"), 
    #function rather than page: 
    path('product/add_to_cart/<int:pk>', add_to_cart_product_detail, name="add_to_cart_product_detail"), 
    #path('product/add_to_cart/<int:pk>/<int:amount>/', add_to_cart_product_detail, name="add_to_cart_product_detail"), 
    path('cart/add_to_cart/<int:pk>', add_to_cart_shopping_cart, name="add_to_cart_shopping_cart"), 
    path('remove_from_cart/<int:pk>', remove_from_cart, name="remove_from_cart"), 
    path('cart/remove_from_cart/<int:pk>', remove_from_cart_shopping_cart, name="remove_from_cart_shopping_cart"), 
    path('cart/quantity_reduce/<int:pk>', quantity_reduce_shopping_cart, name="quantity_reduce_shopping_cart"), 
    path('product/remove_category/<str:type>/<str:name>', remove_category, name="remove_category"), 

    #owner side
    path('item_list/', itemListView.as_view(), name='item-list'), 
    path('upload_item/', upload_new_item_view.as_view(), name='upload-item'), 
    path('update_item/<int:pk>', upload_new_item_view.as_view(), name='update-item'), 
    path('order_list/', OrdersListView.as_view(), name='order-list'), 
    path('order_list/<str:all>', OrdersListView.as_view(), name='order-list-all'), 
    path('remove_item/<int:pk>', remove_item, name='remove-item'), 
    path('modify_homepage/', modify_homepage_config.as_view(), name='home-config'), 
    
]
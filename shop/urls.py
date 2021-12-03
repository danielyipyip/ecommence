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
    itemListView, upload_new_item_view, update_item_view, OrdersListView, modify_homepage_config, modify_layout, modify_category, 
    modify_shop_config, modify_contact_us, 
    remove_item, remove_Season, remove_Type, remove_Gender, edit_Season, edit_Type, edit_Gender, 
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
    path('about_us/', about_page, name='about-us'), 
 
    #function rather than page: 
    path('product/add_to_cart/<int:pk>', add_to_cart_product_detail, name="add_to_cart_product_detail"), 
    #path('product/add_to_cart/<int:pk>/<int:amount>/', add_to_cart_product_detail, name="add_to_cart_product_detail"), 
    path('cart/add_to_cart/<int:pk>', add_to_cart_shopping_cart, name="add_to_cart_shopping_cart"), 
    path('remove_from_cart/<int:pk>', remove_from_cart, name="remove_from_cart"), 
    path('cart/remove_from_cart/<int:pk>', remove_from_cart_shopping_cart, name="remove_from_cart_shopping_cart"), 
    path('cart/quantity_reduce/<int:pk>', quantity_reduce_shopping_cart, name="quantity_reduce_shopping_cart"), 

    path('modify/remove_season/<int:pk>', remove_Season, name="remove_season"), 
    path('modify/remove_type/<int:pk>', remove_Type, name="remove_type"), 
    path('modify/remove_gender/<int:pk>', remove_Gender, name="remove_gender"), 
    path('modify/edit_season/<int:pk>', edit_Season, name="edit_season"), 
    path('modify/edit_type/<int:pk>', edit_Type, name="edit_type"), 
    path('modify/edit_gender/<int:pk>', edit_Gender, name="edit_gender"), 

    #owner side
    path('item_list/', itemListView.as_view(), name='item-list'), 
    path('upload_item/', upload_new_item_view.as_view(), name='upload-item'), 
    path('update_item/<int:pk>', upload_new_item_view.as_view(), name='update-item'), 
    path('order_list/', OrdersListView.as_view(), name='order-list'), 
    path('order_list/<str:all>', OrdersListView.as_view(), name='order-list-all'), 
    path('remove_item/<int:pk>', remove_item, name='remove-item'), 
    path('modify/', modify_layout.as_view(), name='config-all'), 
    path('modify/homepage/', modify_homepage_config.as_view(), name='home-config'), 
    path('modify/category/', modify_category.as_view(), name='category-config'), 
    path('modify/links/', modify_shop_config.as_view(), name='link-config'), 
    path('modify/contactUs/', modify_contact_us.as_view(), name='contact-config'), 

    
]
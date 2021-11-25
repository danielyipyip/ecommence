from django.contrib import admin
from .models import Item, OrderItem, Order, Address, UserProfile, homepage_config, Season_choice, Type_choice, Gender_choice, contact_us_config, page_link, shop_config
# Register your models here.

admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)
admin.site.register(UserProfile)
admin.site.register(homepage_config)
admin.site.register(Season_choice)
admin.site.register(Type_choice)
admin.site.register(Gender_choice)

admin.site.register(contact_us_config)
admin.site.register(page_link)
admin.site.register(shop_config)

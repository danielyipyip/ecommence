from django.contrib import admin
from .models import Item, OrderItem, Order, Address, UserProfile, homepage_config, Season_choice, Type_choice, Gender_choice
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

from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from .views import homePage, productDetailPage

app_name='shop'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', homePage.as_view(), name='home-page'), 
    path('product/<int:pk>', productDetailPage.as_view(), name='product-detail'), 
]
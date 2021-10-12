from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from .views import homePage

app_name='shop'

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', homePage.as_view(), name='home-page'), 
]
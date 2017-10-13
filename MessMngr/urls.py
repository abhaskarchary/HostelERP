from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'^$', views=mess_home, name='mess_home'),
    url(r'^additems$', views=add_items, name='add_items')
]
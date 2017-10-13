from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'^$', views=inventory_logs, name='inventory_logs')
]
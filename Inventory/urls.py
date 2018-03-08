from django.conf.urls import url, include
from . import views

urlpatterns = [

    url(r'^view/$', views.inventory_logs, name='inventory_logs'),
    url(r'^add/$', views.add, name='add'),
    url(r'^add_items/$', views.add_items, name='add_items'),
    url(r'^update/$', views.update, name='update'),
    url(r'^update_items/$', views.update_items, name='update_items'),
    url(r'^new/$', views.new, name='New_item_form'),
    url(r'^newitem/$', views.new_item, name='New_item'),
    url(r'^view_items/$', views.view_items, name='View_items'),
]
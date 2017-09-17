from django.conf.urls import url, include
from django.shortcuts import redirect
from django.views.generic import ListView

from manager.models import EmployeeInfo
from . import views

urlpatterns = [
    #url(r'^$', views.manager, name='manager'),
    url(r'^$', ListView.as_view(queryset=EmployeeInfo.objects.all(), template_name="displayaccounts.html")),
    #url(r'^view/$', views.viewempdata, name='viewempdata'),
    url(r'^register/$', views.register, name='register'),
    url(r'^startsession/$', views.startsession, name='startsession'),
    url(r'^update/$', views.update, name='update'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
]
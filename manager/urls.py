from django.conf.urls import url, include
from django.shortcuts import redirect
from django.views.generic import ListView
from payfees.views import deduct_fees

from manager.models import EmployeeInfo
from . import views

urlpatterns = [
    url(r'^$', views.manager, name='manager'),
    #url(r'^$', ListView.as_view(queryset=EmployeeInfo.objects.all(), template_name="displayaccounts.html")),
    url(r'^view/$', views.viewempdata, name='viewempdata'),
    url(r'^register/$', views.register, name='register'),
    url(r'^startsession/$', views.startsession, name='startsession'),
    url(r'^update/$', views.update, name='update'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^initial_fees/$', views.pay_init_fees, name='pay_init_fees'),
    url(r'^deduct_fees/$', deduct_fees, name='deduct_fees'),
    url(r'^all_transactions/$', views.all_transactions, name='all_transactions'),
    url(r'^all_messages/$', views.all_messages, name='all_messages'),
    url(r'^issue_notice/$', views.issue_notice, name='issue_notice'),
    url(r'^send_notice/$', views.send_notice, name='send_notice'),
]
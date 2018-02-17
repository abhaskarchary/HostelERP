"""erp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^register$', views.form, name = 'form'),
    url(r'^update/(?P<sid>ETL[0-9]+)/$', views.update, name='update'),
    url(r'^update/$', views.update, name = 'update'),
    url(r'^changestdinfo/$', views.change_std_info, name = 'change_std_info'),
    url(r'^studentinfo/$', views.studentinfo, name = 'studentinfo'),
    #url(r'^pay_initial_fees/$', views.pay_init_fees, name = 'pay_init_fees'),
    #url(r'^change_info_student/(?P<sid>ETL[0-9]+)/$', views.change_info, name = 'change_info'),
    url(r'^change_student_info/$', views.change_info, name = 'change_info'),
    url(r'^accountlogs/(?P<stu_id>ETL[0-9]+)/$', views.accountlogs, name = 'account_logs'),
    url(r'^view_balance_fee/(?P<stu_id>ETL[0-9]+)/$', views.view_balance_fee, name = 'view_balance_fee'),
    url(r'^messageroom/$', views.messageroom, name = 'messageroom'),
    #url(r'^startsession/$', views.startsession, name='startsession'), Not needed
    url(r'^login/$', views.login, name='login'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^changepassword/(?P<sid>ETL[0-9]+)/$', views.change_password, name='change_password'),
    url(r'^changepass/(?P<sid>ETL[0-9]+)/$', views.change_pass, name='change_pass'),
    url(r'^send_message/$', views.send_message, name='send_message'),
    url(r'^send_contact_message/$', views.send_contact_message, name='send_contact_message'),
    url(r'^noticebox/$', views.noticebox, name='noticebox'),
    url(r'^noticebox/(?P<nid>NO[0-9]+)/$', views.notice, name='notice'),
]

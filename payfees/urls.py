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
from django.views.generic import ListView,DetailView

from django.conf.urls import url, include

from .models import Dues
from . import views

urlpatterns = [

    url(r'info/$', ListView.as_view(queryset=Dues.objects.all(), template_name="payfees/displayreports.html")),
    url(r'^search_student/$', views.search, name = 'search'),
    url(r'^$', views.account, name = 'account'),
    url(r'^show_student_dues/$', views.show, name = 'show'),
    url(r'^update_dues/$', views.update_dues, name = 'update_dues')
]

from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.admin, name='Admin'),
    url(r'^login/$',views.login, name='login'),
    url(r'^register/$',views.register, name='register'),
    url(r'^update/$',views.update, name='update'),
    url(r'^logout/$',views.logout, name='logout'),
]
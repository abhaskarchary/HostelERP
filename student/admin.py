from django.contrib import admin
from .models import Studentinfo,message,ContactUsMessage

# Register your models here.

admin.site.register(Studentinfo)
admin.site.register(message)
admin.site.register(ContactUsMessage)
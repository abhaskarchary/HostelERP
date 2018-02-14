from __future__ import unicode_literals
from django.db import models
import datetime

# Create your models here.


def increment_id():
    last_reg = AdminInfo.objects.all().order_by('adminid').last()
    if not last_reg:
        return 'A' + str(datetime.date.today().year) + '01'
    if str(datetime.date.today().year) != last_reg.empid[1:5]:
        return 'A' + str(datetime.date.today().year) + '01'
    reg_id = last_reg.empid
    reg_int = int(reg_id[5:7])
    new_reg_int = reg_int + 1
    new_reg_id = 'A' + str(str(datetime.date.today().year)) + str(new_reg_int).zfill(2)
    return new_reg_id



class AdminInfo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    sex = models.CharField(max_length=6)
    adhaar = models.CharField(max_length=12)
    mobile_no = models.CharField(max_length=10)
    address_l1 = models.CharField(max_length=100)
    address_l2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=6)
    registration_date = models.DateTimeField(auto_now=True)
    adminid = models.CharField(max_length=20, default=increment_id, editable=False, primary_key=True)
    password = models.CharField(max_length=20)
    session_key = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.adminid
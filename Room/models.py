# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Room(models.Model):
    room_number = models.CharField(max_length=5, primary_key=True, default=None)
    capacity = models.CharField(max_length=5, default= '2')
    vacancy = models.CharField(max_length=5, default= '2')
    rent = models.CharField(max_length=5, default= '6000')
    additional_charges = models.BooleanField(default= False)
    need_maintenance = models.BooleanField(default= False)
    repairs = models.CharField(max_length=8, default= '0')

    def __str__(self):
        return self.room_number


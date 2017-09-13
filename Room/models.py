# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class room:
    room_number = models.CharField(max_length=5, primary_key=True)
    capacity = models.CharField(max_length=5)
    vacancy = models.CharField(max_length=5)
    fixed_charge


from django.db import models
from student.models import Studentinfo

# Create your models here.
from django.shortcuts import render




class Fees(models.Model):
    fees = models.FloatField(max_length = 20)
    security_money = models.FloatField(max_length = 5)
    fine = models.FloatField(max_length = 5)



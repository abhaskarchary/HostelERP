from django.db import models
from student.models import Studentinfo

# Create your models here.
from django.shortcuts import render


class Dues(models.Model):
    sid = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    fees = models.FloatField(max_length=4, null=False)
    #messfees = models.FloatField(max_length=4, null=False)
    securitymoney = models.FloatField(max_length=4, null=False)
    submission_date=models.DateField(auto_now=True)
    totaldue=models.FloatField(max_length=4, null=False)
    fine = models.FloatField(max_length=4)


    def __str__(self):
        return self.sid

class Fees(models.Model):
    fees = models.FloatField(max_length = 5)
    security_money = models.FloatField(max_length = 5)
    fine = models.FloatField(max_length = 5)

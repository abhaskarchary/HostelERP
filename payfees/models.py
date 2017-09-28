from django.db import models
from student.models import Studentinfo
import datetime

# Create your models here.
from django.shortcuts import render




class Fees(models.Model):
    fees = models.FloatField(max_length = 20)
    security_money = models.FloatField(max_length = 5)
    fine = models.FloatField(max_length = 5)

def increment_transaction_id():
    last_booking = TransactionDetails.objects.all().order_by('transaction_id').last()
    if not last_booking:
        return 'Trans#' + str(datetime.date.today().year) + '0000'
    if str(datetime.date.today().year) != last_booking.transaction_id[6:10]:
        return 'Trans#' + str(datetime.date.today().year) + '0000'
    booking_id = last_booking.transaction_id
    booking_int = int(booking_id[10:14])
    new_booking_int = booking_int + 1
    new_booking_id = 'Trans#' + str(str(datetime.date.today().year)) + str(new_booking_int).zfill(4)
    return new_booking_id


class TransactionDetails(models.Model):
    transaction_id = models.CharField(max_length=20, default=increment_transaction_id, editable=False, primary_key=True)
    transaction_date = models.DateTimeField(auto_now=True)
    sid = models.ForeignKey(Studentinfo)
    credit = models.FloatField(max_length=5)
    debit = models.FloatField(max_length=5)
    remarks = models.CharField(max_length=400)
    balance = models.FloatField(max_length = 5)
    transaction_type = models.CharField(max_length=10)
    transaction_mode = models.CharField(max_length=20)

    def __str__(self):
        return self.transaction_id


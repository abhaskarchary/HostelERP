from django.db import models

# Create your models here.
from student.models import Studentinfo
import datetime

def increment_transaction_id():
    last_booking = Transaction_Details.objects.all().order_by('transaction_id').last()
    if not last_booking:
        return 'Trans#' + str(datetime.date.today().year) + '0000'
    if str(datetime.date.today().year) != last_booking.transaction_id[6:10]:
        return 'Trans#' + str(datetime.date.today().year) + '0000'
    booking_id = last_booking.transaction_id
    booking_int = int(booking_id[10:14])
    new_booking_int = booking_int + 1
    new_booking_id = 'Trans#' + str(str(datetime.date.today().year)) + str(new_booking_int).zfill(4)
    return new_booking_id
#
#
# class TransactionDetails(models.Model):
#     transaction_id = models.CharField(max_length=20, default=increment_transaction_id, editable=False, primary_key=True)
#     transaction_date = models.DateTimeField(auto_now=True)
#     sid = models.ForeignKey(Studentinfo)
#     credit = models.FloatField(max_length=5)
#     debit = models.FloatField(max_length=5)
#     remarks = models.CharField(max_length=400)
#     balance = models.FloatField(max_length = 5)
#     transaction_type = models.CharField(max_length=10)
#     transaction_mode = models.CharField(max_length=20)
#
#     def __str__(self):
#         return self.transaction_id


class Transaction_Details(models.Model):
    transaction_id = models.CharField(max_length=20, default=increment_transaction_id, editable=False, primary_key=True)
    transaction_date = models.DateTimeField(auto_now=True)
    sid = models.ForeignKey(Studentinfo)
    payment_mode = models.CharField(max_length=20, editable=False)
    fees_paid = models.FloatField(max_length = 7)
    fine_paid = models.FloatField(max_length = 7)
    remaining_fees = models.FloatField(max_length = 7)
    remaining_fine = models.FloatField(max_length = 7)
    remaining_total = models.FloatField(max_length = 7)

    def __str__(self):
        return self.transaction_id
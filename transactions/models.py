from django.db import models

# Create your models here.
from student.models import Studentinfo
import datetime

def increment_transaction_id():
    last_booking = Transaction_Details.objects.all().order_by('transaction_id').last()
    if not last_booking:
        return 'Trans' + str(datetime.date.today().year) + '0000'
    if str(datetime.date.today().year) != last_booking.transaction_id[5:9]:
        return 'Trans' + str(datetime.date.today().year) + '0000'
    booking_id = last_booking.transaction_id
    booking_int = int(booking_id[9:13])
    new_booking_int = booking_int + 1
    new_booking_id = 'Trans' + str(str(datetime.date.today().year)) + str(new_booking_int).zfill(4)
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
    transaction_date = models.DateTimeField(auto_now=False)
    sid = models.ForeignKey(Studentinfo)
    student_name=models.CharField(max_length=100)
    payment_mode = models.CharField(max_length=20)
    fees_paid = models.FloatField(max_length = 7)
    fine_paid = models.FloatField(max_length = 7)
    remaining_fees = models.FloatField(max_length = 7)
    remaining_fine = models.FloatField(max_length = 7)
    remaining_total = models.FloatField(max_length = 7)
    cheque_dd_no=models.CharField(max_length=50, null=True, blank=True)
    particulars = models.CharField(max_length=150)

    def __str__(self):
        return self.transaction_id
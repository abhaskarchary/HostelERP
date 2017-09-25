# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
from Room.models import Room
import logging

# Create your models here.

def increment_id():
    last_booking = Studentinfo.objects.all().order_by('sid').last()
    if not last_booking:
        return 'ETL' + str(datetime.date.today().year) + '0000'
    if str(datetime.date.today().year) != last_booking.sid[3:7]:
        return 'ETL' + str(datetime.date.today().year) + '0000'
    booking_id = last_booking.sid
    booking_int = int(booking_id[7:11])
    new_booking_int = booking_int + 1
    new_booking_id = 'ETL' + str(str(datetime.date.today().year)) + str(new_booking_int).zfill(4)
    return new_booking_id


def choices():
    return Room.objects.filter(vacancy__gt=0).values('room_number').query


class Studentinfo(models.Model):
    sid = models.CharField(max_length=20, default=increment_id, editable=False, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, limit_choices_to={'room_number__in': choices()})
    prev_room = None
    sex = models.CharField(max_length=6)
    adhaar = models.CharField(max_length=12)
    mobile_no = models.CharField(max_length=10)
    parent_name = models.CharField(max_length=50)
    parent_mobile = models.CharField(max_length=10)
    address_l1 = models.CharField(max_length=100)
    address_l2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=50)
    guardian_mobile = models.CharField(max_length=10)
    institution_name = models.CharField(max_length=30)
    hod_name = models.CharField(max_length=30)
    hod_mobile = models.CharField(max_length=10)
    registration_date = models.DateTimeField(auto_now=True)
    running_dues = models.FloatField(max_length=4, null=False)
    running_fine = models.FloatField(max_length=4)
    total_dues = models.FloatField(max_length=4)
    refundable_security = models.FloatField(max_length=4)
    balance = models.FloatField(max_length=5)

    def __str__(self):
        return self.sid

    def __init__(self, *args, **kwargs):
        super(Studentinfo, self).__init__(*args, **kwargs)
        try:
            self.prev_room = self.room.room_number
        except:
            self.prev_room = '000'

    def save(self, *args, **kwargs):
        if self.prev_room != self.room.room_number:
            if self.prev_room != '000':
                [prev] = Room.objects.filter(room_number=self.prev_room)
                prev.vacancy = str(int(prev.vacancy) + 1)
                prev.save()

            self.room.vacancy = str(int(self.room.vacancy) - 1)
            self.room.save()
        super(Studentinfo, self).save(*args, **kwargs)



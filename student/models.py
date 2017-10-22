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
    #date_of_birth = models.DateTimeField(default='NA',auto_now = False)
    room = models.ForeignKey(Room, limit_choices_to={'room_number__in': choices()})
    #prev_room = None
    sex = models.CharField(max_length=6)
    blood_grp = models.CharField(max_length=3, default='NA')
    adhaar = models.CharField(max_length=12)
    mobile_no = models.CharField(max_length=10)
    parent_name = models.CharField(max_length=50)
    parent_mobile = models.CharField(max_length=10)
    address_l1 = models.CharField(max_length=100)
    address_l2 = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=10)
    guardian_name = models.CharField(max_length=50, default='NA')
    guardian_mobile = models.CharField(max_length=10, default='NA')
    institution_name = models.CharField(max_length=30)
    #hod_name = models.CharField(max_length=30)
    #hod_mobile = models.CharField(max_length=10)
    registration_date = models.DateTimeField(auto_now=True)
    room_allotment_date = models.DateTimeField(auto_now=True)
    running_dues = models.FloatField(max_length=4, null=False)
    running_fine = models.FloatField(max_length=4)
    total_dues = models.FloatField(max_length=4)
    refundable_security = models.FloatField(max_length=4)
    balance = models.FloatField(max_length=5)
    password = models.CharField(max_length=20, default='123456')
    sessionkey = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    #activated = None

    def __str__(self):
        return self.sid


def message_id():
    last_booking = message.objects.all().order_by('message_id').last()
    if not last_booking:
        return 'SM' + str(datetime.date.today().year) + '0000'
    if str(datetime.date.today().year) != last_booking.message_id[2:6]:
        return 'SM' + str(datetime.date.today().year) + '0000'
    booking_id = last_booking.message_id
    booking_int = int(booking_id[6:10])
    new_booking_int = booking_int + 1
    new_booking_id = 'SM' + str(str(datetime.date.today().year)) + str(new_booking_int).zfill(4)
    return new_booking_id


def notice_id():
    last_booking = Notice.objects.all().order_by('notice_id').last()
    if not last_booking:
        return 'NO' + str(datetime.date.today().year) + '0000'
    if str(datetime.date.today().year) != last_booking.notice_id[2:6]:
        return 'NO' + str(datetime.date.today().year) + '0000'
    booking_id = last_booking.notice_id
    booking_int = int(booking_id[6:10])
    new_booking_int = booking_int + 1
    new_booking_id = 'NO' + str(str(datetime.date.today().year)) + str(new_booking_int).zfill(4)
    return new_booking_id


def msg_id():
    last_booking = ContactUsMessage.objects.all().order_by('msg_id').last()
    if not last_booking:
        return 'CMSG' + str(datetime.date.today().year) + '0001'
    if str(datetime.date.today().year) != last_booking.msg_id[2:6]:
        return 'CMSG' + str(datetime.date.today().year) + '0001'
    booking_id = last_booking.msg_id
    booking_int = int(booking_id[6:10])
    new_booking_int = booking_int + 1
    new_booking_id = 'CMSG' + str(str(datetime.date.today().year)) + str(new_booking_int).zfill(4)
    return new_booking_id


class message(models.Model):
    message_id = models.CharField(max_length=15, default=message_id, editable=False, primary_key=True)
    sender = models.ForeignKey(Studentinfo)
    time_sent = models.DateTimeField(auto_now=True)
    type_of_message = models.CharField(max_length=20)
    body_of_message = models.CharField(max_length=200)

    def __str__(self):
        return self.message_id


class Notice(models.Model):
    notice_id = models.CharField(max_length=15, default=notice_id, editable=False, primary_key=True)
    time_sent = models.DateTimeField(auto_now=True)
    type_of_notice = models.CharField(max_length=20)
    body_of_notice = models.CharField(max_length=200)

    def __str__(self):
        return self.notice_id


class ContactUsMessage(models.Model):
    msg_id = models.CharField(max_length=15, default=msg_id, editable=False, primary_key=True)
    sender_name = models.CharField(max_length=30)
    sender_email = models.CharField(max_length=30)
    time_sent = models.DateTimeField(auto_now=True)
    body_of_message = models.CharField(max_length=200)

    def __str__(self):
        return self.msg_id
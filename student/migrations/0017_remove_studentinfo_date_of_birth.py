# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-12 16:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0016_studentinfo_date_of_birth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentinfo',
            name='date_of_birth',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-08 18:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0014_contactusmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='next_due_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 2, 8, 18, 58, 34, 811376, tzinfo=utc)),
            preserve_default=False,
        ),
    ]

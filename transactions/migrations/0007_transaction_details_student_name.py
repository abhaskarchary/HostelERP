# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-04-15 09:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0006_auto_20180302_0109'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction_details',
            name='student_name',
            field=models.CharField(default='Abhishek chaturvedi', max_length=100),
            preserve_default=False,
        ),
    ]

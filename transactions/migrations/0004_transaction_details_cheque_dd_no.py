# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-01 19:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_auto_20180211_1141'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction_details',
            name='cheque_dd_no',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
    ]
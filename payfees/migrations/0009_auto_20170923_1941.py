# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-23 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payfees', '0008_auto_20170923_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees',
            name='fees',
            field=models.FloatField(max_length=20),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-08 16:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0007_auto_20180308_1856'),
    ]

    operations = [
        migrations.AddField(
            model_name='inventory',
            name='type',
            field=models.CharField(default='purchased', max_length=9),
            preserve_default=False,
        ),
    ]

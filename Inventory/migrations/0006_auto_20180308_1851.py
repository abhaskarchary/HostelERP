# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-08 13:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0005_auto_20180308_1828'),
    ]

    operations = [
        migrations.RenameField(
            model_name='inventoryitems',
            old_name='price',
            new_name='quantity',
        ),
    ]

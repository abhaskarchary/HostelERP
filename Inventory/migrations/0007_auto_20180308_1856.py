# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-08 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Inventory', '0006_auto_20180308_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitems',
            name='unit',
            field=models.CharField(max_length=6, null=True),
        ),
    ]

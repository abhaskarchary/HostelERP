# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-18 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payfees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dues',
            name='sid',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]

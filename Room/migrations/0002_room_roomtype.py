# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-10-18 09:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payfees', '0002_auto_20171018_1508'),
        ('Room', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='roomtype',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='payfees.Fees'),
            preserve_default=False,
        ),
    ]

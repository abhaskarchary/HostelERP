# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-13 05:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('inv_log_id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('quantity', models.CharField(max_length=4)),
                ('price', models.CharField(max_length=5)),
                ('description', models.CharField(blank=True, max_length=30)),
            ],
        ),
    ]

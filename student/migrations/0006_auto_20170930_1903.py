# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 13:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_auto_20170930_1826'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Student_session',
        ),
        migrations.AddField(
            model_name='studentinfo',
            name='session_key',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
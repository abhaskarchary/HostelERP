# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-30 12:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0004_session'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Session',
            new_name='Student_session',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-14 04:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0009_auto_20170111_0111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poem',
            name='tags',
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-09 20:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0006_auto_20170107_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='poem',
            name='profane',
            field=models.BooleanField(default=False),
        ),
    ]
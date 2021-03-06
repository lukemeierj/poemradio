# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-07-11 03:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0002_auto_20160711_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='creation',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='date published'),
        ),
        migrations.AlterField(
            model_name='poem',
            name='source',
            field=models.URLField(blank=True, null=True),
        ),
    ]

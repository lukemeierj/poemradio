# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-05 04:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poemUser', '0012_auto_20161208_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='poemuser',
            name='agreed_tos',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='poemuser',
            name='promo_email',
            field=models.BooleanField(default=False),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-11 00:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0007_poem_profane'),
    ]

    operations = [
        migrations.AddField(
            model_name='poem',
            name='alignment',
            field=models.BooleanField(default=False),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-11 01:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poem', '0008_poem_alignment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='poem',
            old_name='alignment',
            new_name='centered',
        ),
    ]

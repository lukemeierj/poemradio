# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-08 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poemUser', '0011_auto_20161023_1949'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='poemuser',
            name='queue',
        ),
        migrations.AlterField(
            model_name='poemuser',
            name='similar',
            field=models.ManyToManyField(default=[], related_name='_poemuser_similar_+', to='poemUser.PoemUser'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-28 04:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0006_auto_20160713_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='preferred',
            field=models.BooleanField(default=False),
        ),
    ]

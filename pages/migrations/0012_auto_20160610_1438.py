# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-10 14:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0011_auto_20160610_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepage',
            name='politics_quote',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
    ]

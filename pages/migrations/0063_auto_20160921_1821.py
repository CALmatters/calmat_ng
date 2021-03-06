# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-22 01:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0062_proposition_sidebar_markup'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterguide',
            name='headline_image_height',
            field=models.CharField(choices=[('tall', 'Tall'), ('short', 'Short')], default='tall', max_length=30, verbose_name='Headline Image Height'),
        ),
        migrations.AddField(
            model_name='voterguide',
            name='headline_image_offset',
            field=models.CharField(blank=True, default='', max_length=2, verbose_name='Headline Image Offset %'),
        ),
    ]

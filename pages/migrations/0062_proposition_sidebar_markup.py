# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-21 19:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0061_proposition_headline_image_offset'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposition',
            name='sidebar_markup',
            field=models.TextField(blank=True, default='<a class="btn-success countable-send-video" href="#">SEND VIDEO</a>', verbose_name='Sidebar markup'),
        ),
    ]

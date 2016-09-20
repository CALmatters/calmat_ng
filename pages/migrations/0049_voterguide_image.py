# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-19 17:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0004_auto_20160616_1144'),
        ('pages', '0048_voterguide_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterguide',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voterguides_with_image', to='media_manager.MediaItem', verbose_name='Headline image'),
        ),
    ]
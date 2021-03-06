# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-20 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0004_auto_20160616_1144'),
        ('pages', '0054_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterguide',
            name='dark_icon_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voterguides_dark_icon_image', to='media_manager.MediaItem', verbose_name='Dark icon image'),
        ),
        migrations.AlterField(
            model_name='voterguide',
            name='icon_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='voterguides_icon_image', to='media_manager.MediaItem', verbose_name='Light icon image'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 20:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0003_auto_20160607_2028'),
        ('pages', '0016_auto_20160615_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='facebook_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_with_facebook_image', to='media_manager.MediaItem'),
        ),
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='article_with_image', to='media_manager.MediaItem', verbose_name='Featured Image'),
        ),
    ]

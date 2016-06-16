# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-15 20:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0003_auto_20160607_2028'),
        ('pages', '0017_auto_20160615_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='atom',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='atom_with_image', to='media_manager.MediaItem', verbose_name='Featured Image'),
        ),
        migrations.AlterField(
            model_name='atom',
            name='featured_image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='atoms/', verbose_name='Old Featured Image'),
        ),
    ]
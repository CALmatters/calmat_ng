# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-15 02:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0043_voterguide_category_in_menu'),
    ]

    operations = [
        migrations.AddField(
            model_name='proposition',
            name='embedded_content_content',
            field=models.TextField(blank=True, default='', verbose_name='embedded content'),
        ),
        migrations.AddField(
            model_name='proposition',
            name='embedded_content_title',
            field=models.CharField(blank=True, default="Here's How I See It", max_length=50, verbose_name='title'),
        ),
        migrations.AddField(
            model_name='proposition',
            name='video_section_embedded_content',
            field=models.TextField(blank=True, default='', verbose_name='embedded video content'),
        ),
        migrations.AddField(
            model_name='proposition',
            name='video_section_title',
            field=models.CharField(blank=True, default='Show me the money', max_length=50, verbose_name='title'),
        ),
    ]

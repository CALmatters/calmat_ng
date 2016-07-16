# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0023_auto_20160715_1417'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testimonial',
            options={'get_latest_by': 'created', 'ordering': ['order', 'full_name'], 'verbose_name': 'Testimonial', 'verbose_name_plural': 'Testimonials'},
        ),
        migrations.RemoveField(
            model_name='testimonial',
            name='display_order',
        ),
        migrations.AddField(
            model_name='testimonial',
            name='order',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

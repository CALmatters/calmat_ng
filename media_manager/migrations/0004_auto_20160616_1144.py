# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-16 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media_manager', '0003_auto_20160607_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaitem',
            name='creator',
            field=models.CharField(max_length=255, null=True, verbose_name='Photographer / creator'),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='image_type',
            field=models.CharField(choices=[('photo', 'photo'), ('illustration', 'illustration'), ('graphic', 'graphic')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='mediaitem',
            name='license',
            field=models.CharField(choices=[('calmatters owned', 'CALmatters owned'), ('licensed', 'Licensed'), ('creative commons', 'Creative Commons')], max_length=30, null=True),
        ),
    ]

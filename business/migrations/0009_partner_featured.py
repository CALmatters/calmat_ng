# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0008_author_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]

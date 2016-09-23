# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-23 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0065_voterguide_sidebar_markup'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterguide',
            name='show_as_menu',
            field=models.BooleanField(default=False, help_text='If checked, the main menus will show a menu of props or categories.  If not checked the main menus will be a link that leads to a list of propositions.'),
        ),
        migrations.AlterField(
            model_name='voterguide',
            name='category_in_menu',
            field=models.BooleanField(default=True, help_text='If checked, the main menus will show categories.  If not checked the main menus will show propositions.'),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-19 15:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0046_auto_20160916_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='voterguide',
            name='alternate_url',
            field=models.CharField(blank=True, default='/elections/', help_text='i.e. /elections/.  If provided, a LIVE Voter Guide will launch this instead.', max_length=255),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-21 17:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0021_auto_20160620_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='RelatedAtom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atom_layout', models.CharField(choices=[('image', 'Image Layout'), ('embedded', 'Embedded HTML')], default='image', help_text='Home atom layout', max_length=20)),
                ('order', models.PositiveIntegerField(default=0)),
                ('atom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_atom_atoms', to='pages.Atom')),
                ('homepage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_atom_homepages', to='pages.HomePage')),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Related Atom',
                'verbose_name_plural': 'Related Atoms',
            },
        ),
        migrations.AddField(
            model_name='homepage',
            name='atoms',
            field=models.ManyToManyField(blank=True, related_name='homepages_with_atom', through='pages.RelatedAtom', to='pages.Atom', verbose_name='Related Atoms'),
        ),
    ]
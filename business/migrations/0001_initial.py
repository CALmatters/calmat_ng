# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 00:22
from __future__ import unicode_literals

from django.db import migrations, models
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(blank=True, default=b'', max_length=135, verbose_name=b'Description (135 Chars)')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('status', models.IntegerField(choices=[(1, 'Draft'), (2, 'Published')], default=2, help_text='With Draft chosen, will only be shown for admin users on the site.', verbose_name='Status')),
                ('publish_date', models.DateTimeField(blank=True, help_text="With Published chosen, won't be shown until this time", null=True, verbose_name='Published from')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('content', models.TextField(verbose_name='Content')),
                ('job_title', models.CharField(blank=True, default=b'', max_length=100)),
                ('profile_image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=b'authors/', verbose_name=b'Author Image')),
                ('twitter', models.CharField(blank=True, default=b'', help_text=b'Adding a Facebook url will enable Facebook authoring.  i.e. https://www.facebook.com/your_name', max_length=256, verbose_name=b'Twitter @')),
                ('facebook_url', models.CharField(blank=True, default=b'', help_text=b'Adding a Facebook url will enable Facebook authoring.  i.e. https://www.facebook.com/your_name', max_length=256, verbose_name=b'Facebook URL')),
            ],
            options={
                'verbose_name': 'Author',
                'verbose_name_plural': 'Authors',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(blank=True, default=b'', max_length=135, verbose_name=b'Description (135 Chars)')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
                ('partner_type', models.CharField(choices=[(b'distribution', b'Distribution'), (b'data', b'Data')], default=b'distribution', max_length=80)),
                ('link_to_articles', models.BooleanField(default=True, help_text=b'Add link to article list')),
                ('featured_image', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=b'partners/', verbose_name='Featured Image')),
                ('featured_image_large', versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=b'partners/', verbose_name='Featured Image - Large')),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
            },
        ),
        migrations.CreateModel(
            name='PartnerArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fulltext_or_mention', models.CharField(choices=[(b'Not Specified', b'Not Specified'), (b'Full Text Publish', b'Full Text Publish'), (b'Mention/Aggregation', b'Mention/Aggregation')], default=(b'Not Specified', b'Not Specified'), max_length=19, verbose_name=b'Publish Type')),
                ('date_published', models.DateField(blank=True, null=True)),
                ('url', models.CharField(blank=True, default=b'', max_length=255)),
                ('file_upload', models.FileField(blank=True, null=True, upload_to=b'uploads/published')),
                ('print_publish', models.NullBooleanField()),
                ('radio_broadcast', models.NullBooleanField()),
                ('properly_credited', models.NullBooleanField(verbose_name=b'Properly credited?')),
                ('notes', models.TextField(blank=True, default=b'')),
                ('order', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ('order',),
                'verbose_name': 'Distribution',
                'verbose_name_plural': 'Distributions',
            },
        ),
        migrations.CreateModel(
            name='PartnerOwner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.TextField(blank=True, default=b'', max_length=135, verbose_name=b'Description (135 Chars)')),
                ('slug', models.CharField(blank=True, help_text='Leave blank to have the URL auto-generated from the title.', max_length=2000, null=True, verbose_name='URL')),
                ('created', models.DateTimeField(editable=False, null=True)),
                ('updated', models.DateTimeField(editable=False, null=True)),
            ],
            options={
                'ordering': ('title',),
                'verbose_name': 'Owner',
                'verbose_name_plural': 'Owners',
            },
        ),
    ]

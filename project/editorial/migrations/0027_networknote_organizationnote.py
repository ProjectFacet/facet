# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0026_auto_20160111_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='NetworkNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(help_text=b'Content of the note', blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the note was created.', auto_now_add=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', base_field=models.CharField(max_length=100), size=None)),
                ('owner', models.ForeignKey(related_name='networknote_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(help_text=b'Content of the note', blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the note was created.', auto_now_add=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', base_field=models.CharField(max_length=100), size=None)),
                ('owner', models.ForeignKey(related_name='organizationnote_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

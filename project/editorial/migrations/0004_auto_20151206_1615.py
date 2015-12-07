# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0003_auto_20151206_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(help_text=b'Short bio.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='credit_name',
            field=models.CharField(help_text=b'Full name of user as listed as a credit on content.', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='expertise',
            field=django.contrib.postgres.fields.ArrayField(help_text=b'Array of user skills and beats to filter/search by.', base_field=models.CharField(max_length=100), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='user',
            name='organization_id',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(null=True, upload_to=b'users', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='title',
            field=models.CharField(help_text=b'Professional title', max_length=100, unique=True, null=True, blank=True),
        ),
    ]

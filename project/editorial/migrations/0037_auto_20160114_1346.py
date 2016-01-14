# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0036_auto_20160114_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='networknote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organizationnote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='series',
            name='share_with_date',
            field=models.DateTimeField(help_text=b'Estimated date the series will be available', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='seriesnote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seriesnote',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='share_with_date',
            field=models.DateTimeField(help_text=b'Estimated date the story will be available', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='storynote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storynote',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AddField(
            model_name='usernote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usernote',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
    ]

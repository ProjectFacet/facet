# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0048_auto_20160202_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageasset',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
    ]

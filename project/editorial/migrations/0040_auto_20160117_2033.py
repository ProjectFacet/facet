# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0039_user_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='expertise',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'Array of user skills and beats to filter/search by.', size=None, base_field=models.CharField(max_length=255), blank=True),
        ),
    ]

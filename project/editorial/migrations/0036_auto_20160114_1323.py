# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0035_auto_20160113_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='location',
            field=models.CharField(max_length=b'255', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='location',
            field=models.CharField(max_length=b'255', blank=True),
        ),
    ]

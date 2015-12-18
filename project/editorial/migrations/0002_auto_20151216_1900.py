# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0001_cleansweep4'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriesnote',
            name='title',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storynote',
            name='title',
            field=models.CharField(default='test', max_length=255),
            preserve_default=False,
        ),
    ]

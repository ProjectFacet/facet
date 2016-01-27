# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0043_auto_20160126_2010'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='asset_title',
            field=models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True),
        ),
    ]

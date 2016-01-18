# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0040_auto_20160117_2033'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='github',
            field=models.CharField(max_length=250, blank=True),
        ),
    ]

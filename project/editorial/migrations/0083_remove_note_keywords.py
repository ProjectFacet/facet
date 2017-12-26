# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0082_auto_20171226_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='note',
            name='keywords',
        ),
    ]

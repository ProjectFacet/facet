# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0031_auto_20171021_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
    ]

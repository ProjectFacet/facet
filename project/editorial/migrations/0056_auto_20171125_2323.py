# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0055_auto_20171120_2321'),
    ]

    operations = [
        migrations.RenameField(
            model_name='series',
            old_name='series_description',
            new_name='description',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0045_auto_20160201_1442'),
    ]

    operations = [
        migrations.RenameField(
            model_name='network',
            old_name='members',
            new_name='organizations',
        ),
    ]

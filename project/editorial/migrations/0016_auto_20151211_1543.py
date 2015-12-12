# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0015_auto_20151211_0000'),
    ]

    operations = [
        migrations.RenameField(
            model_name='network',
            old_name='organizations',
            new_name='member',
        ),
    ]

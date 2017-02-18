# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0014_videoasset_embed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videoasset',
            name='embed',
        ),
    ]

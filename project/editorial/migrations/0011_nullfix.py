# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0010_auto_20151210_1108'),
    ]

    operations = [
        migrations.RenameField(
            model_name='organization',
            old_name='story_description',
            new_name='org_description',
        ),
    ]

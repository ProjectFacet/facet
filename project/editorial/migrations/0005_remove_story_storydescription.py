# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0004_story_storydescription'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='story',
            name='storydescription',
        ),
    ]

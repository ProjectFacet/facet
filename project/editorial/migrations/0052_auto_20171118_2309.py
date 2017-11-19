# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0051_auto_20171117_1716'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facet',
            old_name='source',
            new_name='sources',
        ),
        migrations.RenameField(
            model_name='historicalfacet',
            old_name='source',
            new_name='sources',
        ),
        migrations.RemoveField(
            model_name='facet',
            name='pushed_to_wp',
        ),
        migrations.RemoveField(
            model_name='historicalfacet',
            name='pushed_to_wp',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0052_auto_20171118_2309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facet',
            old_name='pronunciations',
            new_name='pronounciations',
        ),
        migrations.RenameField(
            model_name='historicalfacet',
            old_name='pronunciations',
            new_name='pronounciations',
        ),
    ]

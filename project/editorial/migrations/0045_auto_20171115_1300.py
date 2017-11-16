# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0044_auto_20171115_1253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facettemplate',
            old_name='fields',
            new_name='fields_used',
        ),
    ]

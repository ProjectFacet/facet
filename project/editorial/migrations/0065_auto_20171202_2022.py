# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0064_auto_20171202_2016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='contributor',
            new_name='contractor',
        ),
    ]

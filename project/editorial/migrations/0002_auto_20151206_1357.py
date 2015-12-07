# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0001_cleansweep'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='fname',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='lname',
            new_name='last_name',
        ),
    ]

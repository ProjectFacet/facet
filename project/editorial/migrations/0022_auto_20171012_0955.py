# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0021_auto_20171012_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='project',
            name='github',
        ),
        migrations.RemoveField(
            model_name='project',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='project',
            name='snapchat',
        ),
        migrations.RemoveField(
            model_name='project',
            name='twitter',
        ),
        migrations.RemoveField(
            model_name='project',
            name='youtube',
        ),
    ]

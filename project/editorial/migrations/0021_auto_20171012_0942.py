# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0020_platform_platformaccount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='facebook',
        ),
        migrations.RemoveField(
            model_name='user',
            name='github',
        ),
        migrations.RemoveField(
            model_name='user',
            name='instagram',
        ),
        migrations.RemoveField(
            model_name='user',
            name='linkedin',
        ),
        migrations.RemoveField(
            model_name='user',
            name='snapchat',
        ),
        migrations.RemoveField(
            model_name='user',
            name='twitter',
        ),
        migrations.RemoveField(
            model_name='user',
            name='vine',
        ),
    ]

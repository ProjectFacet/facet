# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0077_auto_20171218_1258'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='platformaccount',
            unique_together=set([('project', 'name'), ('organization', 'name'), ('project', 'url'), ('user', 'url'), ('user', 'name'), ('organization', 'url')]),
        ),
    ]

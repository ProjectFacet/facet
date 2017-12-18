# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0075_auto_20171218_1251'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='platformaccount',
            unique_together=set([('organization', 'platform', 'url'), ('project', 'platform', 'url'), ('user', 'platform', 'url')]),
        ),
    ]

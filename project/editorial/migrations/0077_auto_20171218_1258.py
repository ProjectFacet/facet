# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0076_auto_20171218_1256'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='platformaccount',
            unique_together=set([('organization', 'url'), ('project', 'url'), ('user', 'url')]),
        ),
    ]

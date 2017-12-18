# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0074_auto_20171216_2326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractorprofile',
            name='public',
            field=models.BooleanField(default=True, help_text=b'Is the contractor publicly listed?'),
        ),
        migrations.AlterUniqueTogether(
            name='platformaccount',
            unique_together=set([('user', 'organization', 'project', 'platform', 'url')]),
        ),
    ]

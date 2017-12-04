# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0066_platformaccount_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractorprofile',
            name='public',
            field=models.BooleanField(default=False, help_text=b'Is the contractor publicly listed?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='public',
            field=models.BooleanField(default=False, help_text=b'If an editor or admin, is the user publicly listed?'),
        ),
    ]

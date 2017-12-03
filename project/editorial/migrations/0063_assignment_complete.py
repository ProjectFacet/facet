# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0062_auto_20171202_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='complete',
            field=models.BooleanField(default=False, help_text=b'Is the assignment complete?'),
        ),
    ]

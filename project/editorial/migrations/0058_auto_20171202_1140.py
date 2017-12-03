# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0057_auto_20171130_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='expiration_date',
            field=models.DateTimeField(help_text=b'Day/Time call ends.', null=True, blank=True),
        ),
    ]

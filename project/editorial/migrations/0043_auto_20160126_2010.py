# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0042_auto_20160126_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='network',
            name='logo',
            field=models.ImageField(upload_to=b'networks', blank=True),
        ),
    ]

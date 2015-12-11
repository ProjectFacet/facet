# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0014_auto_20151210_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='series_id',
            field=models.ForeignKey(blank=True, to='editorial.Series', null=True),
        ),
    ]

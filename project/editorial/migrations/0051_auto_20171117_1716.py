# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0050_auto_20171117_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facet',
            name='story',
            field=models.ForeignKey(to='editorial.Story'),
        ),
    ]

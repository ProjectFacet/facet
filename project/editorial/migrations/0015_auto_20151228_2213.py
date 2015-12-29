# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0014_auto_20151227_1343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofacet',
            name='assets',
            field=models.ManyToManyField(to='editorial.Asset', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='assets',
            field=models.ManyToManyField(to='editorial.Asset', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='assets',
            field=models.ManyToManyField(to='editorial.Asset', blank=True),
        ),
    ]

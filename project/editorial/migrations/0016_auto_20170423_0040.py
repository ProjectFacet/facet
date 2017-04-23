# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0015_remove_videoasset_embed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofacet',
            name='length',
        ),
        migrations.RemoveField(
            model_name='historicalaudiofacet',
            name='length',
        ),
        migrations.RemoveField(
            model_name='historicalprintfacet',
            name='length',
        ),
        migrations.RemoveField(
            model_name='historicalvideofacet',
            name='length',
        ),
        migrations.RemoveField(
            model_name='historicalwebfacet',
            name='length',
        ),
        migrations.RemoveField(
            model_name='printfacet',
            name='length',
        ),
        migrations.RemoveField(
            model_name='videofacet',
            name='length',
        ),
        migrations.RemoveField(
            model_name='webfacet',
            name='length',
        ),
    ]

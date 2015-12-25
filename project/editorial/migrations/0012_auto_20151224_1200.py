# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0011_auto_20151223_0023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofacet',
            name='length',
            field=models.IntegerField(help_text=b'Runtime of the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='length',
            field=models.IntegerField(help_text=b'Runtime of the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='length',
            field=models.IntegerField(help_text=b'Length of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='length',
            field=models.IntegerField(help_text=b'Runtime of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='length',
            field=models.IntegerField(help_text=b'Length of the webfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='length',
            field=models.IntegerField(help_text=b'Length of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='length',
            field=models.IntegerField(help_text=b'Runtime of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='length',
            field=models.IntegerField(help_text=b'Length of the webfacet.', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0012_auto_20151224_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofacet',
            name='captions',
            field=models.TextField(help_text=b'Captions and credits for any assets in use.', blank=True),
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='captions',
            field=models.TextField(help_text=b'Captions and credits for any assets in use.', blank=True),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='captions',
            field=models.TextField(help_text=b'Captions and credits for any assets in use.', blank=True),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='captions',
            field=models.TextField(help_text=b'Captions and credits for any assets in use.', blank=True),
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='captions',
            field=models.TextField(help_text=b'Captions and credits for any assets in use.', blank=True),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='captions',
            field=models.TextField(help_text=b'Captions and credits for any assets in use.', blank=True),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='captions',
            field=models.TextField(help_text=b'Captions and credits for any assets in use.', blank=True),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='captions',
            field=models.TextField(help_text=b'Captions and credits for any assets in use.', blank=True),
        ),
    ]

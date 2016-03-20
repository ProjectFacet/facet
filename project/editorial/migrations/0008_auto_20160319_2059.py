# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0007_auto_20160319_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofacet',
            name='document_assets',
            field=models.ManyToManyField(to='editorial.DocumentAsset', blank=True),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', blank=True),
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', blank=True),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', blank=True),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', blank=True),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='document_assets',
            field=models.ManyToManyField(to='editorial.DocumentAsset', blank=True),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', blank=True),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='document_assets',
            field=models.ManyToManyField(to='editorial.DocumentAsset', blank=True),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', blank=True),
        ),
    ]

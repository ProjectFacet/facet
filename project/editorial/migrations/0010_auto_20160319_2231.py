# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0009_auto_20160319_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofacet',
            name='github_link',
            field=models.URLField(help_text=b'Link to code for any custom feature', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='github_link',
            field=models.URLField(help_text=b'Link to code for any custom feature', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='github_link',
            field=models.URLField(help_text=b'Link to code for any custom feature', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='github_link',
            field=models.URLField(help_text=b'Link to code for any custom feature', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='facebook',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='twitter',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='website',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='facebook',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='github',
            field=models.URLField(max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='instagram',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='linkedin',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='snapchat',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='vine',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='website',
            field=models.URLField(max_length=250, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='github_link',
            field=models.URLField(help_text=b'Link to code for any custom feature', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='github_link',
            field=models.URLField(help_text=b'Link to code for any custom feature', max_length=300, blank=True),
        ),
    ]

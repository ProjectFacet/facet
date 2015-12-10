# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0008_auto_20151209_1619'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='description',
            new_name='asset_description',
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='af_description',
            field=models.TextField(help_text=b'Description of the audiofacet.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='af_description',
            field=models.TextField(help_text=b'Description of the audiofacet.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='pf_description',
            field=models.TextField(help_text=b'Description of the printfacet.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='vf_description',
            field=models.TextField(help_text=b'Description of the videofacet.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='wf_description',
            field=models.TextField(help_text=b'Description of the WebFacet.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='network',
            name='network_description',
            field=models.TextField(help_text=b'Short description of a network.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='story_description',
            field=models.TextField(help_text=b'Short profile of organization.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='pf_description',
            field=models.TextField(help_text=b'Description of the printfacet.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='series',
            name='series_description',
            field=models.TextField(help_text=b'Short description of a series.', blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='story_description',
            field=models.TextField(help_text=b'Short description of a story.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='vf_description',
            field=models.TextField(help_text=b'Description of the videofacet.', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='wf_description',
            field=models.TextField(help_text=b'Description of the WebFacet.', null=True, blank=True),
        ),
    ]

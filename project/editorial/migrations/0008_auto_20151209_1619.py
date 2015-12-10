# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0007_auto_20151207_2336'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalprintfacet',
            name='status',
        ),
        migrations.RemoveField(
            model_name='printfacet',
            name='status',
        ),
        migrations.RemoveField(
            model_name='story',
            name='storydescription',
        ),
        migrations.AlterField(
            model_name='asset',
            name='attribution',
            field=models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='asset',
            name='description',
            field=models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='content',
            field=models.TextField(help_text=b'Content of the audiofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt for the audiofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the audiofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the audiofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='content',
            field=models.TextField(help_text=b'Content of the audiofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt for the audiofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the audiofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the audiofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='content',
            field=models.TextField(help_text=b'Content of the printfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the printfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the printfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='content',
            field=models.TextField(help_text=b'Content of the videofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the videofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the videofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the videofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='content',
            field=models.TextField(help_text=b'Content of the webFacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the Webfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the WebFacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the webfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_logo',
            field=models.ImageField(null=True, upload_to=b'organizations', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='content',
            field=models.TextField(help_text=b'Content of the printfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the printfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the printfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='content',
            field=models.TextField(help_text=b'Content of the videofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the videofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the videofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the videofacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='content',
            field=models.TextField(help_text=b'Content of the webFacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the Webfacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the WebFacet.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the webfacet.', null=True, blank=True),
        ),
    ]

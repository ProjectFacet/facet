# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0018_auto_20160101_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to=settings.AUTH_USER_MODEL, through='editorial.AudioFacetContributor', blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='credit',
            field=models.ManyToManyField(help_text=b'The full user name(s) to be listed as the credit for the facet.', related_name='audiofacetcredit', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to=settings.AUTH_USER_MODEL, through='editorial.PrintFacetContributor', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='credit',
            field=models.ManyToManyField(help_text=b'The full user name(s) to be listed as the credit for the facet.', related_name='printfacetcredit', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to=settings.AUTH_USER_MODEL, through='editorial.VideoFacetContributor', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='credit',
            field=models.ManyToManyField(help_text=b'The full user name(s) to be listed as the credit for the facet.', related_name='videofacetcredit', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='keywords',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
    ]

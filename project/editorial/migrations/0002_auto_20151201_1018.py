# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audiofacet',
            options={'ordering': ['creation_date'], 'verbose_name': 'Audiofacet', 'verbose_name_plural': 'Audiofacets'},
        ),
        migrations.AlterModelOptions(
            name='historicalaudiofacet',
            options={'ordering': ('-history_date', '-history_id'), 'get_latest_by': 'history_date', 'verbose_name': 'historical Audiofacet'},
        ),
        migrations.AlterModelOptions(
            name='historicalprintfacet',
            options={'ordering': ('-history_date', '-history_id'), 'get_latest_by': 'history_date', 'verbose_name': 'historical Printfacet'},
        ),
        migrations.AlterModelOptions(
            name='historicalvideofacet',
            options={'ordering': ('-history_date', '-history_id'), 'get_latest_by': 'history_date', 'verbose_name': 'historical Videofacet'},
        ),
        migrations.AlterModelOptions(
            name='historicalwebfacet',
            options={'ordering': ('-history_date', '-history_id'), 'get_latest_by': 'history_date', 'verbose_name': 'historical Webfacet'},
        ),
        migrations.AlterModelOptions(
            name='printfacet',
            options={'ordering': ['creation_date'], 'verbose_name': 'Printfacet', 'verbose_name_plural': 'Printfacets'},
        ),
        migrations.AlterModelOptions(
            name='videofacet',
            options={'ordering': ['creation_date'], 'verbose_name': 'Videofacet', 'verbose_name_plural': 'Videofacets'},
        ),
        migrations.AlterModelOptions(
            name='webfacet',
            options={'ordering': ['creation_date'], 'verbose_name': 'Webfacet', 'verbose_name_plural': 'Webfacets'},
        ),
        migrations.RenameField(
            model_name='audiofacetcopydetails',
            old_name='new_id',
            new_name='new_audiofacet_id',
        ),
        migrations.RenameField(
            model_name='audiofacetcopydetails',
            old_name='original_id',
            new_name='original_audiofacet_id',
        ),
        migrations.RenameField(
            model_name='printfacetcopydetails',
            old_name='new_id',
            new_name='new_printfacet_id',
        ),
        migrations.RenameField(
            model_name='printfacetcopydetails',
            old_name='original_id',
            new_name='original_printfacet_id',
        ),
        migrations.RenameField(
            model_name='seriescopydetails',
            old_name='new_id',
            new_name='new_series_id',
        ),
        migrations.RenameField(
            model_name='seriescopydetails',
            old_name='original_id',
            new_name='original_series_id',
        ),
        migrations.RenameField(
            model_name='storycopydetails',
            old_name='new_id',
            new_name='new_story_id',
        ),
        migrations.RenameField(
            model_name='storycopydetails',
            old_name='original_id',
            new_name='original_story_id',
        ),
        migrations.RenameField(
            model_name='videofacetcopydetails',
            old_name='new_id',
            new_name='new_videofacet_id',
        ),
        migrations.RenameField(
            model_name='videofacetcopydetails',
            old_name='original_id',
            new_name='original_videofacet_id',
        ),
        migrations.RenameField(
            model_name='webfacetcopydetails',
            old_name='new_id',
            new_name='new_webfacet_id',
        ),
        migrations.RenameField(
            model_name='webfacetcopydetails',
            old_name='original_id',
            new_name='original_webfacet_id',
        ),
        migrations.RemoveField(
            model_name='audiofacet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='historicalaudiofacet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='historicalprintfacet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='historicalvideofacet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='historicalwebfacet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='printfacet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='videofacet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='webfacet',
            name='description',
        ),
    ]

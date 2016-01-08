# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0022_auto_20160108_0839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofacetcopydetail',
            name='new_audiofacet_id',
        ),
        migrations.RemoveField(
            model_name='audiofacetcopydetail',
            name='original_audiofacet_id',
        ),
        migrations.RemoveField(
            model_name='printfacetcopydetail',
            name='new_printfacet_id',
        ),
        migrations.RemoveField(
            model_name='printfacetcopydetail',
            name='original_printfacet_id',
        ),
        migrations.RemoveField(
            model_name='seriescopydetail',
            name='original_series_id',
        ),
        migrations.RemoveField(
            model_name='seriescopydetail',
            name='partner_series_id',
        ),
        migrations.RemoveField(
            model_name='storycopydetail',
            name='partner_story_id',
        ),
        migrations.RemoveField(
            model_name='videofacetcopydetail',
            name='new_videofacet_id',
        ),
        migrations.RemoveField(
            model_name='videofacetcopydetail',
            name='original_videofacet_id',
        ),
        migrations.RemoveField(
            model_name='webfacetcopydetail',
            name='new_webfacet_id',
        ),
        migrations.RemoveField(
            model_name='webfacetcopydetail',
            name='original_webfacet_id',
        ),
        migrations.AddField(
            model_name='audiofacetcopydetail',
            name='original_audiofacet',
            field=models.ForeignKey(related_name='original_audiofacet_detail', default=True, to='editorial.AudioFacet', help_text=b'Original copy of the audiofacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audiofacetcopydetail',
            name='original_org',
            field=models.ForeignKey(related_name='original_audiofacet_organization', default=True, to='editorial.Organization', help_text=b'Organization that originally created the content.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audiofacetcopydetail',
            name='partner_audiofacet',
            field=models.ForeignKey(related_name='audiofacet_copy', default=1, to='editorial.AudioFacet', help_text=b'The new version of the audiofacet saved by the partner organization.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='printfacetcopydetail',
            name='original_org',
            field=models.ForeignKey(related_name='original_printfacet_organization', default=3, to='editorial.Organization', help_text=b'Organization that originally created the content.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='printfacetcopydetail',
            name='original_printfacet',
            field=models.ForeignKey(related_name='original_printfacet_detail', default=True, to='editorial.PrintFacet', help_text=b'Original copy of the printfacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='printfacetcopydetail',
            name='partner_printfacet',
            field=models.ForeignKey(related_name='printfacet_copy', default=1, to='editorial.PrintFacet', help_text=b'The new version of the printfacet saved by the partner organization.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seriescopydetail',
            name='original_org',
            field=models.ForeignKey(related_name='original_series_organization', default=3, to='editorial.Organization', help_text=b'Organization that originally created the content.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seriescopydetail',
            name='original_series',
            field=models.ForeignKey(related_name='original_series_detail', default=True, to='editorial.Series', help_text=b'Original copy of the series.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='seriescopydetail',
            name='partner_series',
            field=models.ForeignKey(related_name='series_copy', default=1, to='editorial.Series', help_text=b'The new version of the series saved by the partner organization.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storycopydetail',
            name='partner_story',
            field=models.ForeignKey(related_name='story_copy', default=1, to='editorial.Story', help_text=b'The new version of the story saved by the partner organization.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videofacetcopydetail',
            name='original_org',
            field=models.ForeignKey(related_name='original_videofacet_organization', default=3, to='editorial.Organization', help_text=b'Organization that originally created the content.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videofacetcopydetail',
            name='original_videofacet',
            field=models.ForeignKey(related_name='original_videofacet_detail', default=True, to='editorial.VideoFacet', help_text=b'Original copy of the videofacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videofacetcopydetail',
            name='partner_videofacet',
            field=models.ForeignKey(related_name='videofacet_copy', default=1, to='editorial.VideoFacet', help_text=b'The new version of the videofacet saved by the partner organization.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webfacetcopydetail',
            name='original_org',
            field=models.ForeignKey(related_name='original_webfacet_organization', default=3, to='editorial.Organization', help_text=b'Organization that originally created the content.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webfacetcopydetail',
            name='original_webfacet',
            field=models.ForeignKey(related_name='original_webfacet_detail', default=True, to='editorial.WebFacet', help_text=b'Original copy of the webfacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webfacetcopydetail',
            name='partner_webfacet',
            field=models.ForeignKey(related_name='webfacet_copy', default=1, to='editorial.WebFacet', help_text=b'The new version of the webfacet saved by the partner organization.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audiofacetcopydetail',
            name='partner',
            field=models.ForeignKey(related_name='audiofacet_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.'),
        ),
        migrations.AlterField(
            model_name='printfacetcopydetail',
            name='partner',
            field=models.ForeignKey(related_name='printfacet_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.'),
        ),
        migrations.AlterField(
            model_name='seriescopydetail',
            name='partner',
            field=models.ForeignKey(related_name='series_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.'),
        ),
        migrations.AlterField(
            model_name='storycopydetail',
            name='original_org',
            field=models.ForeignKey(related_name='original_story_organization', to='editorial.Organization', help_text=b'Organization that originally created the content.'),
        ),
        migrations.AlterField(
            model_name='storycopydetail',
            name='partner',
            field=models.ForeignKey(related_name='story_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.'),
        ),
        migrations.AlterField(
            model_name='videofacetcopydetail',
            name='partner',
            field=models.ForeignKey(related_name='videofacet_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.'),
        ),
        migrations.AlterField(
            model_name='webfacetcopydetail',
            name='partner',
            field=models.ForeignKey(related_name='webfacet_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.'),
        ),
    ]

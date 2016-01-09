# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0022_auto_20160108_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='audiofacetcopydetail',
            name='partner',
            field=models.ForeignKey(related_name='audiofacet_copying_organization', default=1, to='editorial.Organization', help_text=b'Organization that made the copy.'),
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
            name='partner',
            field=models.ForeignKey(related_name='printfacet_copying_organization', default=1, to='editorial.Organization', help_text=b'Organization that made the copy.'),
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
            name='partner',
            field=models.ForeignKey(related_name='series_copying_organization', default=1, to='editorial.Organization', help_text=b'Organization that made the copy.'),
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
            name='partner',
            field=models.ForeignKey(related_name='story_copying_organization', default=1, to='editorial.Organization', help_text=b'Organization that made the copy.'),
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
            name='partner',
            field=models.ForeignKey(related_name='videofacet_copying_organization', default=1, to='editorial.Organization', help_text=b'Organization that made the copy.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videofacetcopydetail',
            name='partner_videofacet',
            field=models.ForeignKey(related_name='videofacet_copy', default=1, to='editorial.VideoFacet', help_text=b'The new version of the videofacet saved by the partner organization.'),
            preserve_default=False,
        ),
    ]

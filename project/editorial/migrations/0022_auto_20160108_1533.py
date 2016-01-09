# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0021_auto_20160107_1513'),
    ]

    operations = [
        migrations.RenameField(
            model_name='historicalaudiofacet',
            old_name='original_org',
            new_name='organization',
        ),
        migrations.RenameField(
            model_name='historicalprintfacet',
            old_name='original_org',
            new_name='organization',
        ),
        migrations.RenameField(
            model_name='historicalvideofacet',
            old_name='original_org',
            new_name='organization',
        ),
        migrations.RenameField(
            model_name='historicalwebfacet',
            old_name='original_org',
            new_name='organization',
        ),
        migrations.RemoveField(
            model_name='audiofacet',
            name='original_org',
        ),
        migrations.RemoveField(
            model_name='audiofacetcopydetail',
            name='new_audiofacet_id',
        ),
        migrations.RemoveField(
            model_name='audiofacetcopydetail',
            name='original_audiofacet_id',
        ),
        migrations.RemoveField(
            model_name='audiofacetcopydetail',
            name='partner',
        ),
        migrations.RemoveField(
            model_name='printfacet',
            name='original_org',
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
            model_name='printfacetcopydetail',
            name='partner',
        ),
        migrations.RemoveField(
            model_name='seriescopydetail',
            name='original_series_id',
        ),
        migrations.RemoveField(
            model_name='seriescopydetail',
            name='partner',
        ),
        migrations.RemoveField(
            model_name='seriescopydetail',
            name='partner_series_id',
        ),
        migrations.RemoveField(
            model_name='story',
            name='original_org',
        ),
        migrations.RemoveField(
            model_name='storycopydetail',
            name='original_story_id',
        ),
        migrations.RemoveField(
            model_name='storycopydetail',
            name='partner',
        ),
        migrations.RemoveField(
            model_name='storycopydetail',
            name='partner_story_id',
        ),
        migrations.RemoveField(
            model_name='videofacet',
            name='original_org',
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
            model_name='videofacetcopydetail',
            name='partner',
        ),
        migrations.RemoveField(
            model_name='webfacet',
            name='original_org',
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
            model_name='audiofacet',
            name='organization',
            field=models.ForeignKey(default=3, to='editorial.Organization', help_text=b'Organization that owns this audiofacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='original_audiofacet',
            field=models.BooleanField(default=True, help_text=b'Was this audiofacet originally created by a user from this organization?'),
        ),
        migrations.AddField(
            model_name='audiofacetcopydetail',
            name='original_audiofacet',
            field=models.ForeignKey(related_name='original_audiofacet_detail', default=1, to='editorial.AudioFacet', help_text=b'Original copy of the audiofacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='audiofacetcopydetail',
            name='original_org',
            field=models.ForeignKey(related_name='original_audiofacet_organization', default=1, to='editorial.Organization', help_text=b'Organization that originally created the content.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='original_audiofacet',
            field=models.BooleanField(default=True, help_text=b'Was this audiofacet originally created by a user from this organization?'),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='original_printfacet',
            field=models.BooleanField(default=True, help_text=b'Was this printfacet originally created by a user from this organization?'),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='original_videofacet',
            field=models.BooleanField(default=True, help_text=b'Was this videofacet originally created by a user from this organization?'),
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='original_webfacet',
            field=models.BooleanField(default=True, help_text=b'Was this webfacet originally created by a user from this organization?'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='organization',
            field=models.ForeignKey(default=3, to='editorial.Organization', help_text=b'Organization that owns this printfacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='printfacet',
            name='original_printfacet',
            field=models.BooleanField(default=True, help_text=b'Was this printfacet originally created by a user from this organization?'),
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
            field=models.ForeignKey(related_name='original_printfacet_detail', default=3, to='editorial.PrintFacet', help_text=b'Original copy of the printfacet.'),
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
            field=models.ForeignKey(related_name='original_series_detail', default=3, to='editorial.Series', help_text=b'Original copy of the series.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='story',
            name='organization',
            field=models.ForeignKey(default=3, to='editorial.Organization', help_text=b'Organization that owns this story.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='story',
            name='original_story',
            field=models.BooleanField(default=True, help_text=b'Was this story originally created by a user from this organization?'),
        ),
        migrations.AddField(
            model_name='storycopydetail',
            name='original_org',
            field=models.ForeignKey(related_name='original_story_organization', default=3, to='editorial.Organization', help_text=b'Organization that originally created the content.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storycopydetail',
            name='original_story',
            field=models.ForeignKey(related_name='original_story_detail', default=3, to='editorial.Story', help_text=b'Original copy of the story.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videofacet',
            name='organization',
            field=models.ForeignKey(default=3, to='editorial.Organization', help_text=b'Organization that owns this videofacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='videofacet',
            name='original_videofacet',
            field=models.BooleanField(default=True, help_text=b'Was this videofacet originally created by a user from this organization?'),
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
            field=models.ForeignKey(related_name='original_videofacet_detail', default=3, to='editorial.VideoFacet', help_text=b'Original copy of the videofacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webfacet',
            name='organization',
            field=models.ForeignKey(default=3, to='editorial.Organization', help_text=b'Organization that owns this webfacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webfacet',
            name='original_webfacet',
            field=models.BooleanField(default=True, help_text=b'Was this webfacet originally created by a user from this organization?'),
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
            field=models.ForeignKey(related_name='original_webfacet_detail', default=3, to='editorial.WebFacet', help_text=b'Original copy of the webfacet.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='webfacetcopydetail',
            name='partner_webfacet',
            field=models.ForeignKey(related_name='webfacet_copy', default=3, to='editorial.WebFacet', help_text=b'The new version of the webfacet saved by the partner organization.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='webfacetcopydetail',
            name='partner',
            field=models.ForeignKey(related_name='webfacet_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.'),
        ),
    ]

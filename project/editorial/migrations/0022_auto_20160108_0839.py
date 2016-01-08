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
            model_name='printfacet',
            name='original_org',
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
            model_name='videofacet',
            name='original_org',
        ),
        migrations.RemoveField(
            model_name='webfacet',
            name='original_org',
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
            field=models.ForeignKey(related_name='original_organization', default=3, to='editorial.Organization', help_text=b'Organization that originally created the content.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storycopydetail',
            name='original_story',
            field=models.ForeignKey(related_name='original_story_detail', default=True, to='editorial.Story', help_text=b'Original copy of the story.'),
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
        migrations.AlterField(
            model_name='storycopydetail',
            name='partner',
            field=models.ForeignKey(related_name='copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.'),
        ),
        migrations.AlterField(
            model_name='storycopydetail',
            name='partner_story_id',
            field=models.ForeignKey(related_name='copy_story', to='editorial.Story', help_text=b'The new version of the story saved by the partner organization.'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0002_auto_20151201_1018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audiofacetasset',
            name='asset_id',
        ),
        migrations.RemoveField(
            model_name='audiofacetasset',
            name='audiofacet_id',
        ),
        migrations.RemoveField(
            model_name='printfacetasset',
            name='asset_id',
        ),
        migrations.RemoveField(
            model_name='printfacetasset',
            name='printfacet_id',
        ),
        migrations.RemoveField(
            model_name='userseries',
            name='series_id',
        ),
        migrations.RemoveField(
            model_name='userseries',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='userstory',
            name='story_id',
        ),
        migrations.RemoveField(
            model_name='userstory',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='videofacetasset',
            name='asset_id',
        ),
        migrations.RemoveField(
            model_name='videofacetasset',
            name='videofacet_id',
        ),
        migrations.RemoveField(
            model_name='webfacetasset',
            name='asset_id',
        ),
        migrations.RemoveField(
            model_name='webfacetasset',
            name='webfacet_id',
        ),
        migrations.RemoveField(
            model_name='historicalaudiofacet',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='historicalprintfacet',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='historicalvideofacet',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='historicalwebfacet',
            name='contributors',
        ),
        migrations.RemoveField(
            model_name='series',
            name='shared_with',
        ),
        migrations.RemoveField(
            model_name='story',
            name='collaborate',
        ),
        migrations.RemoveField(
            model_name='story',
            name='share',
        ),
        migrations.RemoveField(
            model_name='story',
            name='shared_with',
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='assets',
            field=models.ManyToManyField(to='editorial.Asset'),
        ),
        migrations.AddField(
            model_name='network',
            name='organizations',
            field=models.ManyToManyField(related_name='network_organization', through='editorial.NetworkOrganizaton', to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='assets',
            field=models.ManyToManyField(to='editorial.Asset'),
        ),
        migrations.AddField(
            model_name='series',
            name='archived',
            field=models.BooleanField(default=False, help_text=b'Is the content no longer active and needed?'),
        ),
        migrations.AddField(
            model_name='series',
            name='series_team',
            field=models.ManyToManyField(help_text=b'User contributing to the series.', related_name='series_team_member', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='series',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a series is shared with.', related_name='series_shared_with_network', to='editorial.Network'),
        ),
        migrations.AddField(
            model_name='story',
            name='archived',
            field=models.BooleanField(default=False, help_text=b'Is the content no longer active and needed?'),
        ),
        migrations.AddField(
            model_name='story',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a story is shared with.', related_name='story_shared_with_network', to='editorial.Network'),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='assets',
            field=models.ManyToManyField(to='editorial.Asset'),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='assets',
            field=models.ManyToManyField(to='editorial.Asset'),
        ),
        migrations.RemoveField(
            model_name='audiofacet',
            name='contributors',
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to='editorial.User', through='editorial.AudioFacetContributors'),
        ),
        migrations.AlterField(
            model_name='network',
            name='network_owner_organization',
            field=models.ForeignKey(help_text=b'Organization that owns the network.', to='editorial.Organization'),
        ),
        migrations.RemoveField(
            model_name='printfacet',
            name='contributors',
        ),
        migrations.AddField(
            model_name='printfacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to='editorial.User', through='editorial.PrintFacetContributors'),
        ),
        migrations.RemoveField(
            model_name='privatediscussion',
            name='users',
        ),
        migrations.AddField(
            model_name='privatediscussion',
            name='users',
            field=models.ManyToManyField(to='editorial.User'),
        ),
        migrations.RemoveField(
            model_name='series',
            name='collaborate_with',
        ),
        migrations.AddField(
            model_name='series',
            name='collaborate_with',
            field=models.ManyToManyField(help_text=b'Network ids that a series is open to collaboration with.', related_name='series_collaborated_with_network', to='editorial.Network'),
        ),
        migrations.AlterField(
            model_name='series',
            name='series_owner',
            field=models.ForeignKey(related_name='series_owner', to='editorial.User', help_text=b'The user that created the series.'),
        ),
        migrations.RemoveField(
            model_name='story',
            name='collaborate_with',
        ),
        migrations.AddField(
            model_name='story',
            name='collaborate_with',
            field=models.ManyToManyField(help_text=b'Network ids that a story is open to collaboration with.', related_name='story_collaborated_with_network', to='editorial.Network'),
        ),
        migrations.AlterField(
            model_name='story',
            name='story_owner',
            field=models.ForeignKey(related_name='story_owner', to='editorial.User', help_text=b'User who created the story'),
        ),
        migrations.RemoveField(
            model_name='story',
            name='story_team',
        ),
        migrations.AddField(
            model_name='story',
            name='story_team',
            field=models.ManyToManyField(help_text=b'User contributing to the story.', related_name='story_team_member', to='editorial.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_facebook',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_instagram',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_linkedin',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_snapchat',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_twitter',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_vine',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
        migrations.RemoveField(
            model_name='videofacet',
            name='contributors',
        ),
        migrations.AddField(
            model_name='videofacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to='editorial.User', through='editorial.VideoFacetContributors'),
        ),
        migrations.RemoveField(
            model_name='webfacet',
            name='contributors',
        ),
        migrations.AddField(
            model_name='webfacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to='editorial.User', through='editorial.WebFacetContributors'),
        ),
        migrations.DeleteModel(
            name='AudioFacetAsset',
        ),
        migrations.DeleteModel(
            name='PrintFacetAsset',
        ),
        migrations.DeleteModel(
            name='UserSeries',
        ),
        migrations.DeleteModel(
            name='UserStory',
        ),
        migrations.DeleteModel(
            name='VideoFacetAsset',
        ),
        migrations.DeleteModel(
            name='WebFacetAsset',
        ),
    ]

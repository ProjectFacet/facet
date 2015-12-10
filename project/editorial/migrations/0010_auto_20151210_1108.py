# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0009_fixdescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asset',
            name='asset_description',
            field=models.TextField(default='default', help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asset',
            name='attribution',
            field=models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='af_description',
            field=models.TextField(default='default', help_text=b'Description of the audiofacet.', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='code',
            field=models.CharField(default='\x1b[A\x1b[A\x1b[\x1b[B\x1b[Cdefault', help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='content',
            field=models.TextField(default='default', help_text=b'Content of the audiofacet.', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt for the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='af_description',
            field=models.TextField(help_text=b'Description of the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='content',
            field=models.TextField(help_text=b'Content of the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt for the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the audiofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='content',
            field=models.TextField(help_text=b'Content of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='pf_description',
            field=models.TextField(help_text=b'Description of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='content',
            field=models.TextField(help_text=b'Content of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='vf_description',
            field=models.TextField(help_text=b'Description of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='content',
            field=models.TextField(help_text=b'Content of the webFacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the Webfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the WebFacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the webfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='wf_description',
            field=models.TextField(help_text=b'Description of the WebFacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='network_description',
            field=models.TextField(help_text=b'Short description of a network.', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_logo',
            field=models.ImageField(upload_to=b'organizations', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='story_description',
            field=models.TextField(help_text=b'Short profile of organization.', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='content',
            field=models.TextField(help_text=b'Content of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='pf_description',
            field=models.TextField(help_text=b'Description of the printfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='collaborate_with',
            field=models.ManyToManyField(help_text=b'Network ids that a series is open to collaboration with.', related_name='series_collaborated_with_network', to='editorial.Network', blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a series is shared with.', related_name='series_shared_with_network', to='editorial.Network', blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='team',
            field=models.ManyToManyField(help_text=b'User contributing to the series.', related_name='series_team_member', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='story_description',
            field=models.TextField(help_text=b'Short description of a story.', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(help_text=b'Short bio.', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.SlugField(help_text=b'Unique code for a user.', max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='credit_name',
            field=models.CharField(help_text=b'Full name of user as listed as a credit on content.', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='expertise',
            field=django.contrib.postgres.fields.ArrayField(default=list, help_text=b'Array of user skills and beats to filter/search by.', size=None, base_field=models.CharField(max_length=100), blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='facebook',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='instagram',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='linkedin',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='organization_id',
            field=models.ForeignKey(to='editorial.Organization', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(upload_to=b'users', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='snapchat',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='title',
            field=models.CharField(help_text=b'Professional title', unique=True, max_length=100, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='vine',
            field=models.CharField(max_length=150, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='content',
            field=models.TextField(help_text=b'Content of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='vf_description',
            field=models.TextField(help_text=b'Description of the videofacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='code',
            field=models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='content',
            field=models.TextField(help_text=b'Content of the webFacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='excerpt',
            field=models.TextField(help_text=b'Excerpt from the Webfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='length',
            field=models.IntegerField(help_text=b'Wordcount of the WebFacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='share_note',
            field=models.TextField(help_text=b'Information for organizations making a copy of the webfacet.', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='wf_description',
            field=models.TextField(help_text=b'Description of the WebFacet.', blank=True),
        ),
    ]

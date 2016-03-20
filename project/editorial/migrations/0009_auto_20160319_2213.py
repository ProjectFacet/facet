# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0008_auto_20160319_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.BooleanField(default=True, help_text=b'This content originally belonged to this organization.')),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset.', max_length=300, blank=True)),
                ('attribution', models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200, blank=True)),
                ('audio', models.FileField(upload_to=b'audio', blank=True)),
                ('link', models.TextField(help_text=b'Link to audio file on SoundCloud', max_length=400, blank=True)),
                ('audio_type', models.CharField(help_text=b'The kind of audio.', max_length=20, choices=[(b'MP3', b'mp3'), (b'WAV', b'wav'), (b'SC', b'SoundCloud')])),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
                ('organization', models.ForeignKey(related_name='audio_asset_organization', to='editorial.Organization')),
                ('owner', models.ForeignKey(related_name='audio_asset_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Audio Asset',
                'verbose_name_plural': 'Audio Assets',
            },
        ),
        migrations.CreateModel(
            name='VideoAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.BooleanField(default=True, help_text=b'This content originally belonged to this organization.')),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset.', max_length=300, blank=True)),
                ('attribution', models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200, blank=True)),
                ('video', models.FileField(upload_to=b'videos', blank=True)),
                ('link', models.TextField(help_text=b'Link to video file on YouTube or Vimeo', max_length=400, blank=True)),
                ('video_type', models.CharField(help_text=b'The kind of video.', max_length=20, choices=[(b'MP4', b'mp4'), (b'YOUTUBE', b'YouTube'), (b'VIMEO', b'Vimeo')])),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
                ('organization', models.ForeignKey(related_name='video_asset_organization', to='editorial.Organization')),
                ('owner', models.ForeignKey(related_name='video_asset_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Video Asset',
                'verbose_name_plural': 'Video Assets',
            },
        ),
        migrations.AlterField(
            model_name='documentasset',
            name='doc_type',
            field=models.CharField(help_text=b'The kind of document.', max_length=20, choices=[(b'PDF', b'Adobe PDF'), (b'WORD DOC', b'Word Doc'), (b'TEXT', b'Text File'), (b'COMMA SEPARATED', b'Comma Separated'), (b'EXCEL', b'Excel File'), (b'OTHER', b'Other')]),
        ),
        migrations.AlterField(
            model_name='imageasset',
            name='image_type',
            field=models.CharField(help_text=b'The kind of image.', max_length=20, choices=[(b'PIC', b'Photograph'), (b'GRAPH', b'Graphic')]),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='audio_assets',
            field=models.ManyToManyField(to='editorial.AudioAsset', blank=True),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='video_assets',
            field=models.ManyToManyField(to='editorial.VideoAsset', blank=True),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='audio_assets',
            field=models.ManyToManyField(to='editorial.AudioAsset', blank=True),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='video_assets',
            field=models.ManyToManyField(to='editorial.VideoAsset', blank=True),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='audio_assets',
            field=models.ManyToManyField(to='editorial.AudioAsset', blank=True),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='video_assets',
            field=models.ManyToManyField(to='editorial.VideoAsset', blank=True),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='audio_assets',
            field=models.ManyToManyField(to='editorial.AudioAsset', blank=True),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='video_assets',
            field=models.ManyToManyField(to='editorial.VideoAsset', blank=True),
        ),
    ]

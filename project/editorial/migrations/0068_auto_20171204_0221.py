# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0067_auto_20171203_2026'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pitch',
            old_name='audio_assets',
            new_name='simple_audio_assets',
        ),
        migrations.RenameField(
            model_name='pitch',
            old_name='document_assets',
            new_name='simple_document_assets',
        ),
        migrations.RenameField(
            model_name='pitch',
            old_name='image_assets',
            new_name='simple_image_assets',
        ),
        migrations.RenameField(
            model_name='pitch',
            old_name='video_assets',
            new_name='simple_video_assets',
        ),
        migrations.AddField(
            model_name='assignment',
            name='simple_audio_assets',
            field=models.ManyToManyField(to='editorial.SimpleAudio', blank=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='simple_document_assets',
            field=models.ManyToManyField(to='editorial.SimpleDocument', blank=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='simple_image_assets',
            field=models.ManyToManyField(to='editorial.SimpleImage', blank=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='simple_video_assets',
            field=models.ManyToManyField(to='editorial.SimpleVideo', blank=True),
        ),
        migrations.AddField(
            model_name='call',
            name='simple_audio_assets',
            field=models.ManyToManyField(to='editorial.SimpleAudio', blank=True),
        ),
        migrations.AddField(
            model_name='call',
            name='simple_document_assets',
            field=models.ManyToManyField(to='editorial.SimpleDocument', blank=True),
        ),
        migrations.AddField(
            model_name='call',
            name='simple_image_assets',
            field=models.ManyToManyField(to='editorial.SimpleImage', blank=True),
        ),
        migrations.AddField(
            model_name='call',
            name='simple_video_assets',
            field=models.ManyToManyField(to='editorial.SimpleVideo', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='simple_audio_assets',
            field=models.ManyToManyField(to='editorial.SimpleAudio', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='simple_document_assets',
            field=models.ManyToManyField(to='editorial.SimpleDocument', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='simple_image_assets',
            field=models.ManyToManyField(to='editorial.SimpleImage', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='simple_video_assets',
            field=models.ManyToManyField(to='editorial.SimpleVideo', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='simple_audio_assets',
            field=models.ManyToManyField(to='editorial.SimpleAudio', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='simple_document_assets',
            field=models.ManyToManyField(to='editorial.SimpleDocument', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='simple_image_assets',
            field=models.ManyToManyField(to='editorial.SimpleImage', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='simple_video_assets',
            field=models.ManyToManyField(to='editorial.SimpleVideo', blank=True),
        ),
        migrations.AddField(
            model_name='series',
            name='simple_audio_assets',
            field=models.ManyToManyField(to='editorial.SimpleAudio', blank=True),
        ),
        migrations.AddField(
            model_name='series',
            name='simple_document_assets',
            field=models.ManyToManyField(to='editorial.SimpleDocument', blank=True),
        ),
        migrations.AddField(
            model_name='series',
            name='simple_image_assets',
            field=models.ManyToManyField(to='editorial.SimpleImage', blank=True),
        ),
        migrations.AddField(
            model_name='series',
            name='simple_video_assets',
            field=models.ManyToManyField(to='editorial.SimpleVideo', blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='simple_audio_assets',
            field=models.ManyToManyField(to='editorial.SimpleAudio', blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='simple_document_assets',
            field=models.ManyToManyField(to='editorial.SimpleDocument', blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='simple_image_assets',
            field=models.ManyToManyField(to='editorial.SimpleImage', blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='simple_video_assets',
            field=models.ManyToManyField(to='editorial.SimpleVideo', blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='simple_audio_assets',
            field=models.ManyToManyField(to='editorial.SimpleAudio', blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='simple_document_assets',
            field=models.ManyToManyField(to='editorial.SimpleDocument', blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='simple_image_assets',
            field=models.ManyToManyField(to='editorial.SimpleImage', blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='simple_video_assets',
            field=models.ManyToManyField(to='editorial.SimpleVideo', blank=True),
        ),
    ]

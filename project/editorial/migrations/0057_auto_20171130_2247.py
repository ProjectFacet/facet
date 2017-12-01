# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0056_auto_20171125_2323'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationcontractorinfo',
            name='status',
            field=models.BooleanField(default=True, help_text=b'Is this contractor currently working for the organization?'),
        ),
        migrations.AddField(
            model_name='pitch',
            name='audio_assets',
            field=models.ManyToManyField(to='editorial.SimpleAudio', blank=True),
        ),
        migrations.AddField(
            model_name='pitch',
            name='document_assets',
            field=models.ManyToManyField(to='editorial.SimpleDocument', blank=True),
        ),
        migrations.AddField(
            model_name='pitch',
            name='image_assets',
            field=models.ManyToManyField(to='editorial.SimpleImage', blank=True),
        ),
        migrations.AddField(
            model_name='pitch',
            name='video_assets',
            field=models.ManyToManyField(to='editorial.SimpleVideo', blank=True),
        ),
        migrations.AlterField(
            model_name='contractorinfo',
            name='resume',
            field=models.FileField(help_text=b'PDF of contractor resume.', upload_to=b'resumes/%Y/%m/%d', blank=True),
        ),
    ]

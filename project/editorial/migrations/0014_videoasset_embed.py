# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0013_auto_20160629_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='videoasset',
            name='embed',
            field=embed_video.fields.EmbedVideoField(help_text=b'Field for django embed', blank=True),
        ),
    ]

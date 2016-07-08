# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0010_auto_20160319_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audioasset',
            name='link',
            field=models.URLField(help_text=b'Link to audio file on SoundCloud', max_length=400, blank=True),
        ),
        migrations.AlterField(
            model_name='videoasset',
            name='link',
            field=models.URLField(help_text=b'Link to video file on YouTube or Vimeo', max_length=400, blank=True),
        ),
    ]

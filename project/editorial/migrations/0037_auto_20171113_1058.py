# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0036_auto_20171109_1054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audioasset',
            old_name='audio_type',
            new_name='asset_type',
        ),
        migrations.RenameField(
            model_name='audioasset',
            old_name='asset_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='audioasset',
            old_name='asset_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='documentasset',
            old_name='doc_type',
            new_name='asset_type',
        ),
        migrations.RenameField(
            model_name='documentasset',
            old_name='asset_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='documentasset',
            old_name='asset_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='imageasset',
            old_name='asset_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='imageasset',
            old_name='asset_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='simpleaudio',
            old_name='asset_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='simpleaudio',
            old_name='asset_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='simpledocument',
            old_name='asset_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='simpledocument',
            old_name='asset_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='simpleimage',
            old_name='asset_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='simpleimage',
            old_name='asset_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='simplevideo',
            old_name='asset_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='simplevideo',
            old_name='asset_title',
            new_name='title',
        ),
        migrations.RenameField(
            model_name='videoasset',
            old_name='video_type',
            new_name='asset_type',
        ),
        migrations.RenameField(
            model_name='videoasset',
            old_name='asset_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='videoasset',
            old_name='asset_title',
            new_name='title',
        ),
        migrations.RemoveField(
            model_name='imageasset',
            name='image_type',
        ),
        migrations.AddField(
            model_name='imageasset',
            name='asset_type',
            field=models.CharField(default='PIC', help_text=b'The kind of image.', max_length=20, choices=[(b'PIC', b'Photograph'), (b'GRAPH', b'Graphic or Illustration')]),
            preserve_default=False,
        ),
    ]

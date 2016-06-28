# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0011_auto_20160319_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioAssetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('original_audioasset', models.ForeignKey(related_name='original_audioasset_detail', to='editorial.AudioAsset', help_text=b'Original copy of the audioasset')),
                ('original_org', models.ForeignKey(related_name='original_audioasset_organization', to='editorial.Organization', help_text=b'Organization that originally created the content')),
                ('partner', models.ForeignKey(related_name='audioasset_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.')),
                ('partner_audioasset', models.ForeignKey(related_name='audioasset_copy', to='editorial.AudioAsset', help_text=b'The copied version of the audioasset saved by the partner organization.')),
            ],
        ),
        migrations.CreateModel(
            name='DocumentAssetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('original_documentasset', models.ForeignKey(related_name='original_documentasset_detail', to='editorial.DocumentAsset', help_text=b'Original copy of the documentasset')),
                ('original_org', models.ForeignKey(related_name='original_documentasset_organization', to='editorial.Organization', help_text=b'Organization that originally created the content')),
                ('partner', models.ForeignKey(related_name='documentasset_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.')),
                ('partner_documentasset', models.ForeignKey(related_name='documentasset_copy', to='editorial.DocumentAsset', help_text=b'The copied version of the documentasset saved by the partner organization.')),
            ],
        ),
        migrations.CreateModel(
            name='ImageAssetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('original_imageasset', models.ForeignKey(related_name='original_imageasset_detail', to='editorial.ImageAsset', help_text=b'Original copy of the imageasset')),
                ('original_org', models.ForeignKey(related_name='original_imageasset_organization', to='editorial.Organization', help_text=b'Organization that originally created the content')),
                ('partner', models.ForeignKey(related_name='imageasset_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.')),
                ('partner_imageasset', models.ForeignKey(related_name='imageasset_copy', to='editorial.ImageAsset', help_text=b'The copied version of the imageasset saved by the partner organization.')),
            ],
        ),
        migrations.CreateModel(
            name='VideoAssetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('original_org', models.ForeignKey(related_name='original_videoasset_organization', to='editorial.Organization', help_text=b'Organization that originally created the content')),
                ('original_videoasset', models.ForeignKey(related_name='original_videoasset_detail', to='editorial.VideoAsset', help_text=b'Original copy of the videoasset')),
                ('partner', models.ForeignKey(related_name='videoasset_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.')),
                ('partner_videoasset', models.ForeignKey(related_name='videoasset_copy', to='editorial.VideoAsset', help_text=b'The copied version of the videoasset saved by the partner organization.')),
            ],
        ),
    ]

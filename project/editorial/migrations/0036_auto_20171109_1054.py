# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0035_auto_20171107_1141'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleAudio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('audio', models.FileField(upload_to=b'audio', blank=True)),
                ('link', models.URLField(help_text=b'Link to audio file on SoundCloud', max_length=400, blank=True)),
                ('organization', models.ForeignKey(to='editorial.Organization')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SimpleDocument',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('document', models.FileField(upload_to=b'documents', blank=True)),
                ('organization', models.ForeignKey(to='editorial.Organization')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SimpleVideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('video', models.FileField(upload_to=b'videos', blank=True)),
                ('link', models.URLField(help_text=b'Link to video file on YouTube or Vimeo', max_length=400, blank=True)),
                ('organization', models.ForeignKey(to='editorial.Organization')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='governingdocumentasset',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='governingdocumentasset',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='projectdocumentasset',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='projectdocumentasset',
            name='owner',
        ),
        migrations.AlterModelOptions(
            name='audioasset',
            options={},
        ),
        migrations.AlterModelOptions(
            name='documentasset',
            options={},
        ),
        migrations.AlterModelOptions(
            name='imageasset',
            options={},
        ),
        migrations.AlterModelOptions(
            name='simpleimage',
            options={},
        ),
        migrations.AlterModelOptions(
            name='videoasset',
            options={},
        ),
        migrations.RemoveField(
            model_name='facet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='historicalfacet',
            name='description',
        ),
        migrations.RemoveField(
            model_name='project',
            name='governing_document_assets',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_document_assets',
        ),
        migrations.AlterField(
            model_name='audioasset',
            name='asset_description',
            field=models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='audioasset',
            name='organization',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AlterField(
            model_name='audioasset',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='contentlicense',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', help_text=b'Organization that owns this license.', null=True),
        ),
        migrations.AlterField(
            model_name='documentasset',
            name='asset_description',
            field=models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='documentasset',
            name='organization',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AlterField(
            model_name='documentasset',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='videoasset',
            name='asset_description',
            field=models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True),
        ),
        migrations.AlterField(
            model_name='videoasset',
            name='organization',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AlterField(
            model_name='videoasset',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='GoverningDocumentAsset',
        ),
        migrations.DeleteModel(
            name='ProjectDocumentAsset',
        ),
    ]

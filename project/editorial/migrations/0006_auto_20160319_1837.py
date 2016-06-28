# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0005_auto_20160303_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.BooleanField(default=True, help_text=b'This content originally belonged to this organization.')),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset.', max_length=300, blank=True)),
                ('attribution', models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200, blank=True)),
                ('document', models.FileField(upload_to=b'documents', blank=True)),
                ('doc_type', models.CharField(help_text=b'What kind of image.', max_length=20, choices=[(b'PDF', b'Adobe PDF'), (b'WORD DOC', b'Graphic'), (b'TEXT', b'Text File'), (b'COMMA SEPARATED', b'Comma Separated'), (b'EXCEL', b'Excel File'), (b'OTHER', b'Other')])),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
                ('organization', models.ForeignKey(related_name='document_asset_organization', to='editorial.Organization')),
                ('owner', models.ForeignKey(related_name='document_asset_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', blank=True),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='github_link',
            field=models.TextField(help_text=b'Link to code for any custom feature', blank=True),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='document_assets',
            field=models.ManyToManyField(to='editorial.DocumentAsset', blank=True),
        ),
    ]

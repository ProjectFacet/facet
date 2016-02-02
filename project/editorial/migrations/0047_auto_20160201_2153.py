# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0046_auto_20160201_1508'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True)),
                ('attribution', models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200, blank=True)),
                ('photo', models.ImageField(upload_to=b'photos', blank=True)),
                ('image_type', models.CharField(help_text=b'What kind of image.', max_length=20, choices=[(b'PIC', b'Photograph'), (b'GRAPH', b'Graphic')])),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('owner', models.ForeignKey(related_name='asset_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='asset',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='audiofacet',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='printfacet',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='series',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='videofacet',
            name='assets',
        ),
        migrations.RemoveField(
            model_name='webfacet',
            name='assets',
        ),
        migrations.DeleteModel(
            name='Asset',
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='image_assets',
            field=models.ManyToManyField(to='editorial.ImageAsset', blank=True),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='image_assets',
            field=models.ManyToManyField(to='editorial.ImageAsset', blank=True),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='image_assets',
            field=models.ManyToManyField(to='editorial.ImageAsset', blank=True),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='image_assets',
            field=models.ManyToManyField(to='editorial.ImageAsset', blank=True),
        ),
    ]

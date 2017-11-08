# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0034_auto_20171105_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300, blank=True)),
                ('photo', models.ImageField(upload_to=b'photos', blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('organization', models.ForeignKey(to='editorial.Organization')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Simple Image',
                'verbose_name_plural': 'Simple Images',
            },
        ),
        migrations.AlterField(
            model_name='imageasset',
            name='organization',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AlterField(
            model_name='imageasset',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

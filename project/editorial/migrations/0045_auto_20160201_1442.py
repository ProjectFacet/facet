# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0044_asset_asset_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='series',
            name='collaborate_with',
            field=models.ManyToManyField(help_text=b'Organization ids that a series is open to collaboration with.', related_name='series_collaborated_with_organization', to='editorial.Organization', blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='collaborate_with',
            field=models.ManyToManyField(help_text=b'Organization ids that a series is open to collaboration with.', related_name='story_collaborated_with_organization', to='editorial.Organization', blank=True),
        ),
    ]

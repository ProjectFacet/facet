# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0012_audioassetcopydetail_documentassetcopydetail_imageassetcopydetail_videoassetcopydetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalwebfacet',
            name='pushed_to_wp',
            field=models.BooleanField(default=False, help_text=b'Whether the webfacet has been pushed to the organization WordPress site.'),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='pushed_to_wp',
            field=models.BooleanField(default=False, help_text=b'Whether the webfacet has been pushed to the organization WordPress site.'),
        ),
    ]

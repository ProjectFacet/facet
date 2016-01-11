# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0024_auto_20160109_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='organization',
            field=models.ForeignKey(related_name='series_organization', default=3, to='editorial.Organization', help_text=b'The organization a series is associated with.'),
            preserve_default=False,
        ),
    ]

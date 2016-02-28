# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0003_auto_20160219_1711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a story is shared with.', related_name='story_shared_with_network', to='editorial.Network', blank=True),
        ),
    ]

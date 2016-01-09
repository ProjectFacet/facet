# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0023_auto_20160108_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='collaborate_with',
            field=models.ManyToManyField(help_text=b'Network ids that a story is open to collaboration with.', related_name='story_collaborated_with_network', null=True, to='editorial.Network', blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a story is shared with.', related_name='story_shared_with_network', null=True, to='editorial.Network', blank=True),
        ),
    ]

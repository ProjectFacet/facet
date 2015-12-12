# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0016_auto_20151211_1543'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='collaborate',
            field=models.BooleanField(default=False, help_text=b'The story is being collaborated on with a network.'),
        ),
        migrations.AddField(
            model_name='story',
            name='ready_to_share',
            field=models.BooleanField(default=False, help_text=b'The story is finished and ready to be copied.'),
        ),
        migrations.AddField(
            model_name='story',
            name='share',
            field=models.BooleanField(default=False, help_text=b'The story is being shared with a network.'),
        ),
        migrations.AlterField(
            model_name='series',
            name='sensitivity',
            field=models.BooleanField(default=False, help_text=b'Is a series sensitive, for limited viewing?'),
        ),
    ]

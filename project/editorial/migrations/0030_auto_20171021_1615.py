# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0029_auto_20171021_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='organization',
            field=models.ForeignKey(default=1, to='editorial.Organization'),
            preserve_default=False,
        ),
    ]

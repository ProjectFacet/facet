# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0017_auto_20170525_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectnote',
            name='project',
            field=models.ForeignKey(related_name='projectnote', default=1, to='editorial.Project'),
            preserve_default=False,
        ),
    ]

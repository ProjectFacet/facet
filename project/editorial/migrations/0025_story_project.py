# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0024_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='project',
            field=models.ForeignKey(blank=True, to='editorial.Project', null=True),
        ),
    ]

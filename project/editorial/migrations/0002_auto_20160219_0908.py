# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='privatemessage',
            options={'ordering': ['date'], 'verbose_name': 'Private Message', 'verbose_name_plural': 'Private Messages'},
        ),
    ]

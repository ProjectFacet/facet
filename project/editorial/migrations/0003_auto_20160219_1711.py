# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0002_auto_20160219_0908'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='imageasset',
            options={'verbose_name': 'Image', 'verbose_name_plural': 'Images'},
        ),
    ]

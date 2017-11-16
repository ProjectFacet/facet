# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0047_auto_20171115_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractorinfo',
            name='current_location',
            field=models.TextField(help_text=b"Contractor's specific location.", blank=True),
        ),
    ]

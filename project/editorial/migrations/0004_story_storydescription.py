# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0003_auto_20151207_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='storydescription',
            field=models.TextField(help_text=b'Short description of a story.', blank=True),
        ),
    ]

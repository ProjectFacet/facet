# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0006_story_storydescription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='embargo_datetime',
            field=models.DateTimeField(help_text=b'When is the story no longer under embargo.', null=True, blank=True),
        ),
    ]

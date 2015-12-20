# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0008_auto_20151219_0226'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of planning discussion for a story.', null=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of planning discussion for a series.', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0016_auto_20151229_2156'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='original_org',
            field=models.ForeignKey(related_name='story_org', default=3, to='editorial.Organization', help_text=b'Organization the story was originally created by.'),
            preserve_default=False,
        ),
    ]

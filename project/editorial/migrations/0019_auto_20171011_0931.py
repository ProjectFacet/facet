# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0018_projectnote_project'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='sensitivity',
            new_name='sensitive',
        ),
        migrations.RenameField(
            model_name='series',
            old_name='sensitivity',
            new_name='sensitive',
        ),
        migrations.AlterField(
            model_name='story',
            name='name',
            field=models.CharField(help_text=b'The name by which the story is identified.', max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='title',
            field=models.CharField(help_text=b'Professional title.', max_length=100, blank=True),
        ),
    ]

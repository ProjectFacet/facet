# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0083_remove_note_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='note_type',
            field=models.CharField(default='User', help_text=b'The kind of object this note is for.', max_length=25, choices=[(b'ORG', b'Organization'), (b'NET', b'Network'), (b'USER', b'User'), (b'PRO', b'Project'), (b'SER', b'Series'), (b'STO', b'Story'), (b'TSK', b'Task'), (b'EV', b'Event')]),
            preserve_default=False,
        ),
    ]

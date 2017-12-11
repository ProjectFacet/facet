# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0069_auto_20171206_0616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discussion',
            name='discussion_type',
            field=models.CharField(help_text=b'What kind of discussion is it.', max_length=25, choices=[(b'ORG', b'Organization Conversation'), (b'NET', b'Network Conversation'), (b'PRI', b'Private Conversation'), (b'PRO', b'Project Conversation'), (b'SER', b'Series Conversation'), (b'STO', b'Story Conversation'), (b'F', b'Facet Conversation'), (b'TSK', b'Task Conversation'), (b'EV', b'Event Conversation')]),
        ),
    ]

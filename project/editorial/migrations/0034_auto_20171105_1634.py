# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0033_event_evt_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='upload',
        ),
        migrations.AddField(
            model_name='event',
            name='text',
            field=models.TextField(help_text=b'Description of the event.', blank=True),
        ),
    ]

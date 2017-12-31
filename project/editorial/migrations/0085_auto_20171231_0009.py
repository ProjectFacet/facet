# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0084_note_note_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_type',
            field=models.CharField(help_text=b'Kind of event.', max_length=50, choices=[(b'Hosting', b'Hosting'), (b'Reporting', b'Reporting'), (b'Administrative', b'Administrative'), (b'Other', b'Other')]),
        ),
    ]

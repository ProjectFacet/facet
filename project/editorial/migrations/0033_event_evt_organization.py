# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0032_remove_event_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='evt_organization',
            field=models.ForeignKey(related_name='evt_organization', blank=True, to='editorial.Organization', null=True),
        ),
    ]

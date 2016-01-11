# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0025_series_organization'),
    ]

    operations = [
        migrations.AddField(
            model_name='privatemessage',
            name='subject',
            field=models.TextField(help_text=b'The topic of the message.', blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='organization',
            field=models.ForeignKey(related_name='series_organization', to='editorial.Organization', help_text=b'The org'),
        ),
    ]

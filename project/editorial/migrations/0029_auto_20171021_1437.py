# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0028_auto_20171019_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_type',
            field=models.CharField(default='Reporting', help_text=b'Kind of event.', max_length=50, choices=[(b'Hosting', b'Hosting'), (b'Reporting', b'Reporting'), (b'Other', b'Other')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='owner',
            field=models.ForeignKey(related_name='eventowner', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='upload',
            field=models.FileField(null=True, upload_to=b'event/%Y/%m/%d/', blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='upload',
            field=models.FileField(null=True, upload_to=b'task/%Y/%m/%d/', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('editorial', '0023_auto_20171012_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(help_text=b'Name of the event.')),
                ('description', models.TextField(help_text=b'Description of the event.', blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'Date and time event is created.', auto_now_add=True)),
                ('event_date', models.DateTimeField(help_text=b'Date and time of the event.', blank=True)),
                ('venue', models.TextField(help_text=b'The location of the event.', blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('team', models.ManyToManyField(help_text=b'The users assigned to an event.', related_name='eventteam', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
    ]

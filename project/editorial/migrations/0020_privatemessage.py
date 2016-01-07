# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0019_auto_20160105_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(help_text=b'The content of the message.')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('discussion', models.ForeignKey(to='editorial.Discussion')),
                ('recipient', models.ForeignKey(related_name='private_message_recipient', to=settings.AUTH_USER_MODEL, help_text=b'The recipient of the private message.')),
                ('user', models.ForeignKey(related_name='private_message_sender', to=settings.AUTH_USER_MODEL, help_text=b'The sender of the private message.')),
            ],
        ),
    ]

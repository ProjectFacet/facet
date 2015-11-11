# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.SlugField(help_text=b'Unique code for a user.', max_length=15, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=45, db_index=True)),
                ('last_name', models.CharField(max_length=45, db_index=True)),
                ('username', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254, blank=True)),
                ('phone', models.CharField(max_length=20, blank=True)),
                ('bio', models.TextField(help_text=b'Short bio.', blank=True)),
                ('profile_photo', models.ImageField(upload_to=b'users', blank=True)),
                ('facebook_un', models.CharField(max_length=75)),
                ('twitter_un', models.CharField(max_length=75)),
                ('linkedin_un', models.CharField(max_length=75)),
            ],
        ),
    ]

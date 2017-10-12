# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0019_auto_20171011_0931'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Name of the platform.', max_length=250)),
                ('icon_code', models.CharField(help_text=b'text for font-awesome icon for the platform', max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PlatformAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Short name to identify the social account.', max_length=250, db_index=True)),
                ('url', models.URLField(max_length=250, blank=True)),
                ('organization', models.ForeignKey(to='editorial.Organization', blank=True)),
                ('platform', models.ForeignKey(to='editorial.Platform')),
                ('project', models.ForeignKey(blank=True, to='editorial.Project', null=True)),
                ('team', models.ManyToManyField(help_text=b'User that contributes to this account.', related_name='platform_team_member', to=settings.AUTH_USER_MODEL, blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
    ]

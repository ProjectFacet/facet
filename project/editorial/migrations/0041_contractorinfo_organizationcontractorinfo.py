# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0040_auto_20171115_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractorInfo',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('resume', models.FileField(upload_to=b'resumes/%Y/%m/%d', blank=True)),
                ('address', models.TextField(help_text=b'Mailing address.', blank=True)),
                ('availability', models.TextField(help_text=b'Notes on when a contractor is available or not.', blank=True)),
                ('current_location', models.TextField(help_text=b'Contractors specific location.', blank=True)),
                ('gear', models.TextField(help_text=b'Gear that a contractor has access to and skills for.', blank=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('editorial.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationContractorInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('w9_on_file', models.BooleanField(default=False, help_text=b'Does the organization have a W9 on file.')),
                ('rates', models.TextField(help_text=b'The rates the contractor is paid by the org.', blank=True)),
                ('strengths', models.TextField(help_text=b'Internal notes on strengths of the contractor.', blank=True)),
                ('conflicts', models.TextField(help_text=b'Any conflicts of interest the contractor has.', blank=True)),
                ('editor_notes', models.TextField(help_text=b'Any notes for editors on things to know when working with this contractor.', blank=True)),
            ],
        ),
    ]

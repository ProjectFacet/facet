# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0071_auto_20171216_2240'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscription_type', models.CharField(help_text=b'Type of subscription', max_length=25, choices=[(b'Contractor', b'Contractor'), (b'Organization', b'Organization')])),
                ('collaborations', models.BooleanField(default=False, help_text=b'If an organization is using the account for base features of editorial workflow, project management and collaboration.')),
                ('contractors', models.BooleanField(default=False, help_text=b'If an organization is using the account to manage contractors.')),
                ('standard', models.BooleanField(default=False, help_text=b'Basic use by a contractor')),
                ('user', models.ForeignKey(help_text=b'For Contractor account, that user profile, for Organization, the owner.', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

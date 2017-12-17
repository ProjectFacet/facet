# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0073_accountsubscription_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractorSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('standard', models.BooleanField(default=True, help_text=b'If an organization is using the account for base features of editorial workflow, project management and collaboration.')),
                ('user', models.ForeignKey(help_text=b'User associated with this subscription.', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationSubscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('collaborations', models.BooleanField(default=True, help_text=b'If an organization is using the account for base features of editorial workflow, project management and collaboration.')),
                ('contractors', models.BooleanField(default=False, help_text=b'If an organization is using the account to manage contractors.')),
                ('organization', models.ForeignKey(help_text=b'Organization associated with this subscription if Org subscription type.', to='editorial.Organization')),
            ],
        ),
        migrations.RemoveField(
            model_name='accountsubscription',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='accountsubscription',
            name='user',
        ),
        migrations.DeleteModel(
            name='AccountSubscription',
        ),
    ]

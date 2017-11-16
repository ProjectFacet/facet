# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0048_auto_20171115_2338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformaccount',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='platformaccount',
            name='user',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

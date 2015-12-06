# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0002_auto_20151205_1930'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NetworkOrganizaton',
            new_name='NetworkOrganization',
        ),
        migrations.AlterField(
            model_name='network',
            name='organizations',
            field=models.ManyToManyField(related_name='network_organization', through='editorial.NetworkOrganization', to='editorial.Organization'),
        ),
    ]

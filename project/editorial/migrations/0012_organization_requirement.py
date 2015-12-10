# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0011_nullfix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='organization_id',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
    ]

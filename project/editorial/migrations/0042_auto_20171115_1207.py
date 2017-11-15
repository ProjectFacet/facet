# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0041_contractorinfo_organizationcontractorinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='organizationcontractorinfo',
            name='contractor_info',
            field=models.ForeignKey(default=None, to='editorial.ContractorInfo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organizationcontractorinfo',
            name='organization',
            field=models.ForeignKey(default=None, to='editorial.Organization'),
            preserve_default=False,
        ),
    ]

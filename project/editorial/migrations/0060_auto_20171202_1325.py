# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0059_auto_20171202_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractorinfo',
            name='portfolio_link1',
            field=models.URLField(help_text=b'Link to portfolio item/', max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contractorinfo',
            name='portfolio_link2',
            field=models.URLField(help_text=b'Link to portfolio item/', max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contractorinfo',
            name='portfolio_link3',
            field=models.URLField(help_text=b'Link to portfolio item/', max_length=500, null=True, blank=True),
        ),
    ]

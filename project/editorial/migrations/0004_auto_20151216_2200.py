# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0003_auto_20151216_2155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', null=True, blank=True),
        ),
    ]

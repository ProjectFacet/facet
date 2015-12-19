# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0006_auto_20151217_2235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='audiofacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='due_edit',
            field=models.DateTimeField(help_text=b'Due for edit.', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='run_date',
            field=models.DateTimeField(help_text=b'Planned run date.', null=True, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0026_auto_20171012_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='completion_date',
            field=models.DateTimeField(help_text=b'Date and time task status is changed to complete.', auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='inprogress_date',
            field=models.DateTimeField(help_text=b'Date and time task status is changed to in progress.', null=True, blank=True),
        ),
    ]

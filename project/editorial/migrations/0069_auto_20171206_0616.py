# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0068_auto_20171204_0221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contractorprofile',
            name='resume',
            field=models.FileField(help_text=b'PDF of contractor resume.', null=True, upload_to=b'resumes/%Y/%m/%d', blank=True),
        ),
    ]

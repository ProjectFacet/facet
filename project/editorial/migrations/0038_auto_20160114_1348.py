# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0037_auto_20160114_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='networknote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
        ),
        migrations.AlterField(
            model_name='organizationnote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
        ),
        migrations.AlterField(
            model_name='seriesnote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
        ),
        migrations.AlterField(
            model_name='storynote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
        ),
        migrations.AlterField(
            model_name='usernote',
            name='important',
            field=models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes'),
        ),
    ]

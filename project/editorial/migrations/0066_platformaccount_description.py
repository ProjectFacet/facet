# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0065_auto_20171202_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='platformaccount',
            name='description',
            field=models.TextField(help_text=b'Short description of the purpose of the account.', blank=True),
        ),
    ]

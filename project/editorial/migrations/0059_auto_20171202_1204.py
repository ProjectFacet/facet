# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0058_auto_20171202_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(help_text=b'Type of user.', max_length=25, choices=[(b'Admin', b'Admin'), (b'Editor', b'Editor'), (b'Staff', b'Staff'), (b'Contractor', b'Contractor')]),
        ),
    ]

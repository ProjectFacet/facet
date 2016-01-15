# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0038_auto_20160114_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.CharField(default='Staff', help_text=b'Type of user.', max_length=25, choices=[(b'Admin', b'Admin'), (b'Editor', b'Editor'), (b'Staff', b'Staff')]),
            preserve_default=False,
        ),
    ]

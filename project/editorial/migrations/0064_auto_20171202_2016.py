# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0063_assignment_complete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pitch',
            old_name='contributor',
            new_name='contractor',
        ),
        migrations.AddField(
            model_name='pitch',
            name='recipient',
            field=models.ForeignKey(default=1, to=settings.AUTH_USER_MODEL, help_text=b'To whom is this pitch directed?'),
            preserve_default=False,
        ),
    ]

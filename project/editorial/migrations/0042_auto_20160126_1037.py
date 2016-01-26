# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0041_user_github'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='profile_photo',
            new_name='photo',
        ),
        migrations.AlterField(
            model_name='network',
            name='logo',
            field=models.ImageField(upload_to=b'logos', blank=True),
        ),
    ]

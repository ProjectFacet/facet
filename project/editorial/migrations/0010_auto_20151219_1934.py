# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0009_auto_20151219_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='notes',
            field=models.ManyToManyField(related_name='user_note', to='editorial.UserNote', blank=True),
        ),
    ]

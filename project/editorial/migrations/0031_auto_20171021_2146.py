# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0030_auto_20171021_1615'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['name'], 'verbose_name': 'Task', 'verbose_name_plural': 'Tasks'},
        ),
        migrations.RenameField(
            model_name='task',
            old_name='task_status',
            new_name='status',
        ),
        migrations.RemoveField(
            model_name='task',
            name='title',
        ),
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.TextField(default='Task', help_text=b'Name of the task.'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('editorial', '0022_auto_20171012_0955'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField(help_text=b'Title of the task.')),
                ('text', models.TextField(help_text=b'Content of the task.', blank=True)),
                ('task_status', models.CharField(help_text=b'Task status.', max_length=50, choices=[(b'Identified', b'Identified'), (b'In Progress', b'In Progress'), (b'Complete', b'Complete')])),
                ('important', models.BooleanField(default=False, help_text=b'Whether a task is important.')),
                ('creation_date', models.DateTimeField(help_text=b'Date and time task is created.', auto_now_add=True)),
                ('due_date', models.DateTimeField(help_text=b'Date and time task is to be completed.', blank=True)),
                ('inprogress_date', models.DateTimeField(help_text=b'Date and time task status is changed to in progress.', blank=True)),
                ('completion_date', models.DateTimeField(help_text=b'Date and time task status is changed to complete.', auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('assigned_to', models.ManyToManyField(help_text=b'The users assigned to the task.', related_name='taskassigneduser', to=settings.AUTH_USER_MODEL, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('owner', models.ForeignKey(related_name='taskowner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
            },
        ),
        migrations.AlterModelOptions(
            name='platform',
            options={'ordering': ['name'], 'verbose_name': 'Platform', 'verbose_name_plural': 'Platforms'},
        ),
        migrations.AlterModelOptions(
            name='platformaccount',
            options={'ordering': ['name'], 'verbose_name': 'Platform Account', 'verbose_name_plural': 'Platform Accounts'},
        ),
    ]

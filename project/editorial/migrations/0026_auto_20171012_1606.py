# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0025_story_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='event',
            name='object_id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='task',
            name='object_id',
        ),
        migrations.AddField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='project',
            field=models.ForeignKey(blank=True, to='editorial.Project', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='series',
            field=models.ForeignKey(blank=True, to='editorial.Series', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='story',
            field=models.ForeignKey(blank=True, to='editorial.Story', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='event',
            field=models.ForeignKey(blank=True, to='editorial.Event', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, to='editorial.Project', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='series',
            field=models.ForeignKey(blank=True, to='editorial.Series', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='story',
            field=models.ForeignKey(blank=True, to='editorial.Story', null=True),
        ),
    ]

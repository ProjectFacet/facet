# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0039_auto_20171113_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(help_text=b'Content of the note', blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the note was created.', auto_now_add=True)),
                ('important', models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TaskNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(help_text=b'Content of the note', blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the note was created.', auto_now_add=True)),
                ('important', models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
                ('organization', models.ForeignKey(related_name='tasknote_org', to='editorial.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='task',
            name='upload',
        ),
        migrations.AddField(
            model_name='event',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of discussion for the event.', null=True),
        ),
        migrations.AddField(
            model_name='facet',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of discussion for the facet.', null=True),
        ),
        migrations.AddField(
            model_name='historicalfacet',
            name='discussion',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Discussion', null=True),
        ),
        migrations.AddField(
            model_name='task',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of discussion for the task.', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='public',
            field=models.BooleanField(default=False, help_text=b'If an editor or contributor, is the user publicly listed?'),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='discussion_type',
            field=models.CharField(help_text=b'What kind of discussion is it.', max_length=25, choices=[(b'ORG', b'Organization Conversation'), (b'NET', b'Network Conversation'), (b'PRI', b'Private Conversation'), (b'PRO', b'Project Conversation'), (b'SER', b'Series Conversation'), (b'STO', b'Story Conversation'), (b'F', b'Facet Conversation'), (b'TSK', b'Task Conversation'), (b'EV', b'Event Conversation'), (b'WF', b'WebFacet Conversation'), (b'PF', b'PrintFacet Conversation'), (b'AF', b'AudioFacet Conversation'), (b'VF', b'VideoFacet Conversation')]),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(help_text=b'Type of user.', max_length=25, choices=[(b'Admin', b'Admin'), (b'Editor', b'Editor'), (b'Staff', b'Staff'), (b'Contributor', b'Contributor')]),
        ),
        migrations.AddField(
            model_name='tasknote',
            name='owner',
            field=models.ForeignKey(related_name='tasknote_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tasknote',
            name='task',
            field=models.ForeignKey(to='editorial.Task'),
        ),
        migrations.AddField(
            model_name='eventnote',
            name='event',
            field=models.ForeignKey(to='editorial.Event'),
        ),
        migrations.AddField(
            model_name='eventnote',
            name='organization',
            field=models.ForeignKey(related_name='eventnote_org', to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='eventnote',
            name='owner',
            field=models.ForeignKey(related_name='eventnote_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]

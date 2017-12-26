# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0080_auto_20171224_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(help_text=b'Content of the note', blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the note was created.', auto_now_add=True)),
                ('important', models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='eventnote',
            name='event',
        ),
        migrations.RemoveField(
            model_name='eventnote',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='eventnote',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='networknote',
            name='network',
        ),
        migrations.RemoveField(
            model_name='networknote',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='organizationnote',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='organizationnote',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='projectnote',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='projectnote',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='projectnote',
            name='project',
        ),
        migrations.RemoveField(
            model_name='seriesnote',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='seriesnote',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='seriesnote',
            name='series',
        ),
        migrations.RemoveField(
            model_name='storynote',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='storynote',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='storynote',
            name='story',
        ),
        migrations.RemoveField(
            model_name='tasknote',
            name='organization',
        ),
        migrations.RemoveField(
            model_name='tasknote',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='tasknote',
            name='task',
        ),
        migrations.RemoveField(
            model_name='usernote',
            name='owner',
        ),
        migrations.AlterModelOptions(
            name='pitch',
            options={'verbose_name': 'Pitch', 'verbose_name_plural': 'Pitches'},
        ),
        migrations.AlterField(
            model_name='user',
            name='notes',
            field=models.ManyToManyField(related_name='user_note', to='editorial.Note', blank=True),
        ),
        migrations.DeleteModel(
            name='EventNote',
        ),
        migrations.DeleteModel(
            name='NetworkNote',
        ),
        migrations.DeleteModel(
            name='OrganizationNote',
        ),
        migrations.DeleteModel(
            name='ProjectNote',
        ),
        migrations.DeleteModel(
            name='SeriesNote',
        ),
        migrations.DeleteModel(
            name='StoryNote',
        ),
        migrations.DeleteModel(
            name='TaskNote',
        ),
        migrations.DeleteModel(
            name='UserNote',
        ),
        migrations.AddField(
            model_name='note',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]

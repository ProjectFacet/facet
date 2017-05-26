# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0016_auto_20170423_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoverningDocumentAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.BooleanField(default=True, help_text=b'This content originally belonged to this organization.')),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset.', max_length=300, blank=True)),
                ('attribution', models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200, blank=True)),
                ('document', models.FileField(upload_to=b'governing documents', blank=True)),
                ('doc_type', models.CharField(help_text=b'The kind of document.', max_length=20, choices=[(b'PDF', b'Adobe PDF'), (b'WORD DOC', b'Word Doc'), (b'TEXT', b'Text File'), (b'COMMA SEPARATED', b'Comma Separated'), (b'EXCEL', b'Excel File'), (b'OTHER', b'Other')])),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
                ('organization', models.ForeignKey(related_name='governing_document_asset_organization', to='editorial.Organization')),
                ('owner', models.ForeignKey(related_name='governing_document_asset_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Governing Document',
                'verbose_name_plural': 'Governing Documents',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name identifying the project.', max_length=75)),
                ('project_description', models.TextField(help_text=b'Short description of a project.', blank=True)),
                ('project_logo', models.ImageField(upload_to=b'projects', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('sensitivity', models.BooleanField(default=False, help_text=b'Is a project sensitive, for limited viewing?')),
                ('share', models.BooleanField(default=False, help_text=b'The project is being shared with a network.')),
                ('share_with_date', models.DateTimeField(help_text=b'Estimated date the project will be available', null=True, blank=True)),
                ('collaborate', models.BooleanField(default=False, help_text=b'The project is being collaborated on with a network.')),
                ('archived', models.BooleanField(default=False, help_text=b'Is the content no longer active and needed?')),
                ('website', models.URLField(max_length=250, blank=True)),
                ('github', models.URLField(max_length=300, blank=True)),
                ('facebook', models.URLField(max_length=250, blank=True)),
                ('twitter', models.URLField(max_length=250, blank=True)),
                ('instagram', models.URLField(max_length=250, blank=True)),
                ('snapchat', models.URLField(max_length=250, blank=True)),
                ('youtube', models.URLField(max_length=250, blank=True)),
                ('collaborate_with', models.ManyToManyField(help_text=b'Organization ids that a project is open to collaboration with.', related_name='project_collaborated_with_organization', to='editorial.Organization', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='ProjectDocumentAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original', models.BooleanField(default=True, help_text=b'This content originally belonged to this organization.')),
                ('asset_title', models.CharField(help_text=b'Text for file name. Name it intuitively.', max_length=200, blank=True)),
                ('asset_description', models.TextField(help_text=b'What is the asset.', max_length=300, blank=True)),
                ('attribution', models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200, blank=True)),
                ('document', models.FileField(upload_to=b'project documents', blank=True)),
                ('doc_type', models.CharField(help_text=b'The kind of document.', max_length=20, choices=[(b'PDF', b'Adobe PDF'), (b'WORD DOC', b'Word Doc'), (b'TEXT', b'Text File'), (b'COMMA SEPARATED', b'Comma Separated'), (b'EXCEL', b'Excel File'), (b'OTHER', b'Other')])),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
                ('organization', models.ForeignKey(related_name='project_document_asset_organization', to='editorial.Organization')),
                ('owner', models.ForeignKey(related_name='project_document_asset_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Project Document',
                'verbose_name_plural': 'Project Documents',
            },
        ),
        migrations.CreateModel(
            name='ProjectNote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField(help_text=b'Content of the note', blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When the note was created.', auto_now_add=True)),
                ('important', models.BooleanField(default=False, help_text=b'Mark as important for pinning to top of notes')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for note search.', size=None, base_field=models.CharField(max_length=100), blank=True)),
                ('organization', models.ForeignKey(related_name='projectnote_org', to='editorial.Organization')),
                ('owner', models.ForeignKey(related_name='projectnote_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='discussion',
            name='discussion_type',
            field=models.CharField(help_text=b'What kind of discussion is it.', max_length=25, choices=[(b'ORG', b'Organization Conversation'), (b'NET', b'Network Conversation'), (b'PRI', b'Private Conversation'), (b'PRO', b'Project Conversation'), (b'SER', b'Series Conversation'), (b'STO', b'Story Conversation'), (b'WF', b'WebFacet Conversation'), (b'PF', b'PrintFacet Conversation'), (b'AF', b'AudioFacet Conversation'), (b'VF', b'VideoFacet Conversation')]),
        ),
        migrations.AddField(
            model_name='project',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of planning discussion for a project.', null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='governing_document_assets',
            field=models.ManyToManyField(to='editorial.GoverningDocumentAsset', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(related_name='project_organization', to='editorial.Organization', help_text=b'The org'),
        ),
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(related_name='project_owner', to=settings.AUTH_USER_MODEL, help_text=b'The user that created the project.'),
        ),
        migrations.AddField(
            model_name='project',
            name='project_document_assets',
            field=models.ManyToManyField(to='editorial.ProjectDocumentAsset', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a project is shared with.', related_name='project_shared_with_network', to='editorial.Network', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ManyToManyField(help_text=b'User contributing to the project.', related_name='project_team_member', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]

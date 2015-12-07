# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.contrib.postgres.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.TextField(help_text=b'What is the asset. (If a photo or graphic, it should be the caption.)', max_length=300)),
                ('attribution', models.TextField(help_text=b'The appropriate information for crediting the asset.', max_length=200)),
                ('s3_link', models.URLField(help_text=b'The item on S3.', max_length=300)),
                ('asset_type', models.CharField(help_text=b'What kind is the asset.', max_length=20, choices=[(b'PIC', b'Photograph'), (b'GRAPH', b'Graphic'), (b'AUD', b'Audio'), (b'VID', b'Video'), (b'DOC', b'Document')])),
                ('creation_date', models.DateTimeField(help_text=b'When the asset was created.', auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='AudioFacet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75)),
                ('title', models.TextField(help_text=b'Headline of the audiofacet.')),
                ('excerpt', models.TextField(help_text=b'Excerpt for the audiofacet.')),
                ('content', models.TextField(help_text=b'Content of the audiofacet.')),
                ('length', models.IntegerField(help_text=b'Wordcount of the audiofacet.')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('status', models.CharField(help_text=b'Audiofacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')])),
                ('due_edit', models.DateTimeField(help_text=b'Due for edit.')),
                ('run_date', models.DateTimeField(help_text=b'Planned run date.')),
                ('creation_date', models.DateTimeField(help_text=b'Day audiofacet was created.', auto_now_add=True)),
                ('share_note', models.TextField(help_text=b'Information for organizations making a copy of the audiofacet.')),
                ('assets', models.ManyToManyField(to='editorial.Asset')),
            ],
            options={
                'ordering': ['creation_date'],
                'verbose_name': 'Audiofacet',
                'verbose_name_plural': 'Audiofacets',
            },
        ),
        migrations.CreateModel(
            name='AudioFacetContributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_role', models.CharField(help_text=b'What did the user do?', max_length=255)),
                ('audiofacet_id', models.ForeignKey(to='editorial.AudioFacet')),
            ],
        ),
        migrations.CreateModel(
            name='AudioFacetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new_audiofacet_id', models.SlugField(help_text=b"Id of the story on the copying organization's site.", max_length=15)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(help_text=b'The comment of the comment.')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CommentReadStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime_read', models.DateTimeField(auto_now_add=True)),
                ('has_read', models.BooleanField(default=True)),
                ('comment_id', models.ForeignKey(to='editorial.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discussion_type', models.CharField(help_text=b'What kind of discussion is it.', max_length=25, choices=[(b'PRI', b'Private Conversation'), (b'SER', b'Series Conversation'), (b'STO', b'Story Conversation'), (b'WF', b'WebFacet Conversation'), (b'PF', b'PrintFacet Conversation'), (b'AF', b'AudioFacet Conversation'), (b'VF', b'VideoFacet Conversation')])),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalAudioFacet',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('code', models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75)),
                ('title', models.TextField(help_text=b'Headline of the audiofacet.')),
                ('excerpt', models.TextField(help_text=b'Excerpt for the audiofacet.')),
                ('content', models.TextField(help_text=b'Content of the audiofacet.')),
                ('length', models.IntegerField(help_text=b'Wordcount of the audiofacet.')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('status', models.CharField(help_text=b'Audiofacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')])),
                ('due_edit', models.DateTimeField(help_text=b'Due for edit.')),
                ('run_date', models.DateTimeField(help_text=b'Planned run date.')),
                ('creation_date', models.DateTimeField(help_text=b'Day audiofacet was created.', editable=False, blank=True)),
                ('share_note', models.TextField(help_text=b'Information for organizations making a copy of the audiofacet.')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('discussion_id', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Discussion', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Audiofacet',
            },
        ),
        migrations.CreateModel(
            name='HistoricalPrintFacet',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('code', models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75)),
                ('title', models.TextField(help_text=b'Headline of the printfacet.')),
                ('excerpt', models.TextField(help_text=b'Excerpt from the printfacet.')),
                ('content', models.TextField(help_text=b'Content of the printfacet.')),
                ('length', models.IntegerField(help_text=b'Wordcount of the printfacet.')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('status', models.CharField(help_text=b'Printfacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')])),
                ('due_edit', models.DateTimeField(help_text=b'Due for edit.')),
                ('run_date', models.DateTimeField(help_text=b'Planned run date.')),
                ('creation_date', models.DateTimeField(help_text=b'Day printfacet was created.', editable=False, blank=True)),
                ('share_note', models.TextField(help_text=b'Information for organizations making a copy of the printfacet.')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('discussion_id', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Discussion', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Printfacet',
            },
        ),
        migrations.CreateModel(
            name='HistoricalVideoFacet',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('code', models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75)),
                ('title', models.TextField(help_text=b'Headline of the videofacet.')),
                ('excerpt', models.TextField(help_text=b'Excerpt from the videofacet.')),
                ('content', models.TextField(help_text=b'Content of the videofacet.')),
                ('length', models.IntegerField(help_text=b'Wordcount of the videofacet.')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('status', models.CharField(help_text=b'Videofacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')])),
                ('due_edit', models.DateTimeField(help_text=b'Due for edit.')),
                ('run_date', models.DateTimeField(help_text=b'Planned run date.')),
                ('creation_date', models.DateTimeField(help_text=b'Day videofacet was created.', editable=False, blank=True)),
                ('share_note', models.TextField(help_text=b'Information for organizations making a copy of the videofacet.')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('discussion_id', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Discussion', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Videofacet',
            },
        ),
        migrations.CreateModel(
            name='HistoricalWebFacet',
            fields=[
                ('id', models.IntegerField(verbose_name='ID', db_index=True, auto_created=True, blank=True)),
                ('code', models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75)),
                ('title', models.TextField(help_text=b'Headline of the Webfacet')),
                ('excerpt', models.TextField(help_text=b'Excerpt from the Webfacet.')),
                ('content', models.TextField(help_text=b'Content of the webFacet.')),
                ('length', models.IntegerField(help_text=b'Wordcount of the WebFacet.')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('status', models.CharField(help_text=b'WebFacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')])),
                ('due_edit', models.DateTimeField(help_text=b'Due for edit.')),
                ('run_date', models.DateTimeField(help_text=b'Planned run date.')),
                ('creation_date', models.DateTimeField(help_text=b'Day WebFacet was created.', editable=False, blank=True)),
                ('share_note', models.TextField(help_text=b'Information for organizations making a copy of the webfacet.')),
                ('history_id', models.AutoField(serialize=False, primary_key=True)),
                ('history_date', models.DateTimeField()),
                ('history_type', models.CharField(max_length=1, choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')])),
                ('discussion_id', models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Discussion', null=True)),
            ],
            options={
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
                'verbose_name': 'historical Webfacet',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name by which members identify the network.', max_length=75, db_index=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ImageField(upload_to=b'organizations', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Network',
                'verbose_name_plural': 'Networks',
            },
        ),
        migrations.CreateModel(
            name='NetworkOrganization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('network_id', models.ForeignKey(to='editorial.Network')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=75, db_index=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('organization_logo', models.ImageField(upload_to=b'organizations', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='PrintFacet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75)),
                ('title', models.TextField(help_text=b'Headline of the printfacet.')),
                ('excerpt', models.TextField(help_text=b'Excerpt from the printfacet.')),
                ('content', models.TextField(help_text=b'Content of the printfacet.')),
                ('length', models.IntegerField(help_text=b'Wordcount of the printfacet.')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('status', models.CharField(help_text=b'Printfacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')])),
                ('due_edit', models.DateTimeField(help_text=b'Due for edit.')),
                ('run_date', models.DateTimeField(help_text=b'Planned run date.')),
                ('creation_date', models.DateTimeField(help_text=b'Day printfacet was created.', auto_now_add=True)),
                ('share_note', models.TextField(help_text=b'Information for organizations making a copy of the printfacet.')),
                ('assets', models.ManyToManyField(to='editorial.Asset')),
            ],
            options={
                'ordering': ['creation_date'],
                'verbose_name': 'Printfacet',
                'verbose_name_plural': 'Printfacets',
            },
        ),
        migrations.CreateModel(
            name='PrintFacetContributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_role', models.CharField(help_text=b'What did the user do?', max_length=255)),
                ('printfacet_id', models.ForeignKey(to='editorial.PrintFacet')),
            ],
        ),
        migrations.CreateModel(
            name='PrintFacetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new_printfacet_id', models.SlugField(help_text=b"Id of the story on the copying organization's site.", max_length=15)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('organization_id', models.ForeignKey(help_text=b'Id of the organization that made the copy.', to='editorial.Organization')),
                ('original_printfacet_id', models.ForeignKey(help_text=b'Original id of the story.', to='editorial.PrintFacet')),
            ],
        ),
        migrations.CreateModel(
            name='PrivateDiscussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('discussion_id', models.ForeignKey(to='editorial.Discussion')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name identifying the series.', max_length=75)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('share', models.BooleanField(default=False, help_text=b'The series is being shared with a network.')),
                ('collaborate', models.BooleanField(default=False, help_text=b'The series is being collaborated on with a network.')),
                ('archived', models.BooleanField(default=False, help_text=b'Is the content no longer active and needed?')),
                ('collaborate_with', models.ManyToManyField(help_text=b'Network ids that a series is open to collaboration with.', related_name='series_collaborated_with_network', to='editorial.Network')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Series',
                'verbose_name_plural': 'Series',
            },
        ),
        migrations.CreateModel(
            name='SeriesCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new_series_id', models.SlugField(help_text=b"Id of the series on the copying organization's site.", max_length=15)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('organization_id', models.ForeignKey(help_text=b'Id of the organization that made the copy.', to='editorial.Organization')),
                ('original_series_id', models.ForeignKey(help_text=b'Original id of the series.', to='editorial.Series')),
            ],
        ),
        migrations.CreateModel(
            name='SeriesPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(help_text=b'Notes for planning a series. Can be any details needed to be tracked while a series is planned/reported.')),
            ],
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'The name by which the story is identified', max_length=250)),
                ('embargo', models.BooleanField(default=False, help_text=b'Is a story embargoed?')),
                ('embargo_datetime', models.DateTimeField(help_text=b'When is the story no longer under embargo.')),
                ('sensitivity', models.BooleanField(default=False, help_text=b'Is a story sensitive, for limited viewing?')),
                ('creation_date', models.DateTimeField(help_text=b'When was the story created.', auto_now_add=True)),
                ('archived', models.BooleanField(default=False, help_text=b'Is the content no longer active and needed?')),
                ('collaborate_with', models.ManyToManyField(help_text=b'Network ids that a story is open to collaboration with.', related_name='story_collaborated_with_network', to='editorial.Network')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Story',
                'verbose_name_plural': 'Stories',
            },
        ),
        migrations.CreateModel(
            name='StoryCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new_story_id', models.SlugField(help_text=b"Id of the story on the copying organization's site.", max_length=15)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('organization_id', models.ForeignKey(help_text=b'Id of the organization that made the copy.', to='editorial.Organization')),
                ('original_story_id', models.ForeignKey(help_text=b'Original id of the story.', to='editorial.Story')),
            ],
        ),
        migrations.CreateModel(
            name='StoryPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField(help_text=b'Notes for planning a story. Can be any details needed to be tracked while a story is planned/reported.')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.SlugField(help_text=b'Unique code for a user.', max_length=15, null=True, blank=True)),
                ('first_name', models.CharField(db_index=True, max_length=45, null=True, blank=True)),
                ('last_name', models.CharField(db_index=True, max_length=45, null=True, blank=True)),
                ('credit_name', models.CharField(help_text=b'Full name of user as listed as a credit on content.', max_length=75, null=True, blank=True)),
                ('title', models.CharField(help_text=b'Professional title', max_length=100, unique=True, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=20, null=True, blank=True)),
                ('bio', models.TextField(help_text=b'Short bio.', null=True, blank=True)),
                ('expertise', django.contrib.postgres.fields.ArrayField(help_text=b'Array of user skills and beats to filter/search by.', base_field=models.CharField(max_length=100), blank=True, default=list, null=True, size=None)),
                ('profile_photo', models.ImageField(upload_to=b'users', blank=True)),
                ('facebook', models.CharField(max_length=150, null=True, blank=True)),
                ('twitter', models.CharField(max_length=150, null=True, blank=True)),
                ('linkedin', models.CharField(max_length=150, null=True, blank=True)),
                ('instagram', models.CharField(max_length=150, null=True, blank=True)),
                ('snapchat', models.CharField(max_length=150, null=True, blank=True)),
                ('vine', models.CharField(max_length=150, null=True, blank=True)),
                ('organization_id', models.ForeignKey(blank=True, to='editorial.Organization', null=True)),
            ],
            options={
                'ordering': ['credit_name'],
                'verbose_name': 'Team member',
                'verbose_name_plural': 'Team members',
            },
        ),
        migrations.CreateModel(
            name='VideoFacet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75)),
                ('title', models.TextField(help_text=b'Headline of the videofacet.')),
                ('excerpt', models.TextField(help_text=b'Excerpt from the videofacet.')),
                ('content', models.TextField(help_text=b'Content of the videofacet.')),
                ('length', models.IntegerField(help_text=b'Wordcount of the videofacet.')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('status', models.CharField(help_text=b'Videofacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')])),
                ('due_edit', models.DateTimeField(help_text=b'Due for edit.')),
                ('run_date', models.DateTimeField(help_text=b'Planned run date.')),
                ('creation_date', models.DateTimeField(help_text=b'Day videofacet was created.', auto_now_add=True)),
                ('share_note', models.TextField(help_text=b'Information for organizations making a copy of the videofacet.')),
                ('assets', models.ManyToManyField(to='editorial.Asset')),
            ],
            options={
                'ordering': ['creation_date'],
                'verbose_name': 'Videofacet',
                'verbose_name_plural': 'Videofacets',
            },
        ),
        migrations.CreateModel(
            name='VideoFacetContributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_role', models.CharField(help_text=b'What did the user do?', max_length=255)),
                ('user_id', models.ForeignKey(to='editorial.User')),
                ('videofacet_id', models.ForeignKey(to='editorial.VideoFacet')),
            ],
        ),
        migrations.CreateModel(
            name='VideoFacetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new_videofacet_id', models.SlugField(help_text=b"Id of the story on the copying organization's site.", max_length=15)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('organization_id', models.ForeignKey(help_text=b'Id of the organization that made the copy.', to='editorial.Organization')),
                ('original_videofacet_id', models.ForeignKey(help_text=b'Original id of the story.', to='editorial.VideoFacet')),
            ],
        ),
        migrations.CreateModel(
            name='WebFacet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(help_text=b'Unique code as needed for ingest sytems. Use as needed', max_length=75)),
                ('title', models.TextField(help_text=b'Headline of the Webfacet')),
                ('excerpt', models.TextField(help_text=b'Excerpt from the Webfacet.')),
                ('content', models.TextField(help_text=b'Content of the webFacet.')),
                ('length', models.IntegerField(help_text=b'Wordcount of the WebFacet.')),
                ('keywords', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'List of keywords for search.', base_field=models.CharField(max_length=100), size=None)),
                ('status', models.CharField(help_text=b'WebFacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')])),
                ('due_edit', models.DateTimeField(help_text=b'Due for edit.')),
                ('run_date', models.DateTimeField(help_text=b'Planned run date.')),
                ('creation_date', models.DateTimeField(help_text=b'Day WebFacet was created.', auto_now_add=True)),
                ('share_note', models.TextField(help_text=b'Information for organizations making a copy of the webfacet.')),
                ('assets', models.ManyToManyField(to='editorial.Asset')),
            ],
            options={
                'ordering': ['creation_date'],
                'verbose_name': 'Webfacet',
                'verbose_name_plural': 'Webfacets',
            },
        ),
        migrations.CreateModel(
            name='WebFacetContributor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_role', models.CharField(help_text=b'What did the user do?', max_length=255)),
                ('user_id', models.ForeignKey(to='editorial.User')),
                ('webfacet_id', models.ForeignKey(to='editorial.WebFacet')),
            ],
        ),
        migrations.CreateModel(
            name='WebFacetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('new_webfacet_id', models.SlugField(help_text=b"Id of the story on the copying organization's site.", max_length=15)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('organization_id', models.ForeignKey(help_text=b'Id of the organization that made the copy.', to='editorial.Organization')),
                ('original_webfacet_id', models.ForeignKey(help_text=b'Original id of the story.', to='editorial.WebFacet')),
            ],
        ),
        migrations.AddField(
            model_name='webfacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to='editorial.User', through='editorial.WebFacetContributor'),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='credit',
            field=models.ManyToManyField(help_text=b'The full user name(s) to be listed as the credit for the facet.', related_name='webfacetcredit', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='discussion_id',
            field=models.ForeignKey(help_text=b'Id of edit discussion for the webfacet.', to='editorial.Discussion'),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='editor',
            field=models.ForeignKey(related_name='webfaceteditor', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='original_org',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='owner',
            field=models.ForeignKey(related_name='webfacetowner', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='webfacet',
            name='story_id',
            field=models.ForeignKey(to='editorial.Story'),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to='editorial.User', through='editorial.VideoFacetContributor'),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='credit',
            field=models.ManyToManyField(help_text=b'The full user name(s) to be listed as the credit for the facet.', related_name='videofacetcredit', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='discussion_id',
            field=models.ForeignKey(help_text=b'ID of edit discussion for the videofacet.', to='editorial.Discussion'),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='editor',
            field=models.ForeignKey(related_name='videofaceteditor', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='original_org',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='owner',
            field=models.ForeignKey(related_name='videofacetowner', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='videofacet',
            name='story_id',
            field=models.ForeignKey(to='editorial.Story'),
        ),
        migrations.AddField(
            model_name='storyplan',
            name='note_owner',
            field=models.ForeignKey(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='storyplan',
            name='story_discussion_id',
            field=models.ForeignKey(to='editorial.Discussion'),
        ),
        migrations.AddField(
            model_name='storyplan',
            name='story_id',
            field=models.ForeignKey(to='editorial.Story'),
        ),
        migrations.AddField(
            model_name='story',
            name='owner',
            field=models.ForeignKey(related_name='story_owner', to='editorial.User', help_text=b'User who created the story'),
        ),
        migrations.AddField(
            model_name='story',
            name='series_id',
            field=models.ForeignKey(to='editorial.Series'),
        ),
        migrations.AddField(
            model_name='story',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a story is shared with.', related_name='story_shared_with_network', to='editorial.Network'),
        ),
        migrations.AddField(
            model_name='story',
            name='team',
            field=models.ManyToManyField(help_text=b'User contributing to the story.', related_name='story_team_member', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='seriesplan',
            name='note_owner',
            field=models.ForeignKey(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='seriesplan',
            name='series_discussion_id',
            field=models.ForeignKey(to='editorial.Discussion'),
        ),
        migrations.AddField(
            model_name='seriesplan',
            name='series_id',
            field=models.ForeignKey(to='editorial.Series'),
        ),
        migrations.AddField(
            model_name='series',
            name='owner',
            field=models.ForeignKey(related_name='series_owner', to='editorial.User', help_text=b'The user that created the series.'),
        ),
        migrations.AddField(
            model_name='series',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a series is shared with.', related_name='series_shared_with_network', to='editorial.Network'),
        ),
        migrations.AddField(
            model_name='series',
            name='team',
            field=models.ManyToManyField(help_text=b'User contributing to the series.', related_name='series_team_member', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='privatediscussion',
            name='users',
            field=models.ManyToManyField(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='printfacetcontributor',
            name='user_id',
            field=models.ForeignKey(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to='editorial.User', through='editorial.PrintFacetContributor'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='credit',
            field=models.ManyToManyField(help_text=b'The full user name(s) to be listed as the credit for the facet.', related_name='printfacetcredit', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='discussion_id',
            field=models.ForeignKey(help_text=b'Id of edit discussion for the printfacet.', to='editorial.Discussion'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='editor',
            field=models.ForeignKey(related_name='printfaceteditor', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='original_org',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='owner',
            field=models.ForeignKey(related_name='printfacetowner', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='printfacet',
            name='story_id',
            field=models.ForeignKey(to='editorial.Story'),
        ),
        migrations.AddField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='networkorganization',
            name='organization_id',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='network',
            name='organizations',
            field=models.ManyToManyField(related_name='network_organization', through='editorial.NetworkOrganization', to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='network',
            name='owner_organization',
            field=models.ForeignKey(help_text=b'Organization that owns the network.', to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='editor',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.User', null=True),
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='history_user',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='original_org',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='owner',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.User', null=True),
        ),
        migrations.AddField(
            model_name='historicalwebfacet',
            name='story_id',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Story', null=True),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='editor',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.User', null=True),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='history_user',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='original_org',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='owner',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.User', null=True),
        ),
        migrations.AddField(
            model_name='historicalvideofacet',
            name='story_id',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Story', null=True),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='editor',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.User', null=True),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='history_user',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='original_org',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='owner',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.User', null=True),
        ),
        migrations.AddField(
            model_name='historicalprintfacet',
            name='story_id',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Story', null=True),
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='editor',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.User', null=True),
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='history_user',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='original_org',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='owner',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.User', null=True),
        ),
        migrations.AddField(
            model_name='historicalaudiofacet',
            name='story_id',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.Story', null=True),
        ),
        migrations.AddField(
            model_name='commentreadstatus',
            name='user_id',
            field=models.ForeignKey(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='comment',
            name='discussion_id',
            field=models.ForeignKey(to='editorial.Discussion'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_id',
            field=models.ForeignKey(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='audiofacetcopydetail',
            name='organization_id',
            field=models.ForeignKey(help_text=b'Id of the organization that made the copy.', to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='audiofacetcopydetail',
            name='original_audiofacet_id',
            field=models.ForeignKey(help_text=b'Original id of the story.', to='editorial.AudioFacet'),
        ),
        migrations.AddField(
            model_name='audiofacetcontributor',
            name='user_id',
            field=models.ForeignKey(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to='editorial.User', through='editorial.AudioFacetContributor'),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='credit',
            field=models.ManyToManyField(help_text=b'The full user name(s) to be listed as the credit for the facet.', related_name='audiofacetcredit', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='discussion_id',
            field=models.ForeignKey(help_text=b'Id of edit discussion for the audiofacet.', to='editorial.Discussion'),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='editor',
            field=models.ForeignKey(related_name='audiofaceteditor', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='original_org',
            field=models.ForeignKey(to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='owner',
            field=models.ForeignKey(related_name='audiofacetowner', to='editorial.User'),
        ),
        migrations.AddField(
            model_name='audiofacet',
            name='story_id',
            field=models.ForeignKey(to='editorial.Story'),
        ),
        migrations.AddField(
            model_name='asset',
            name='owner',
            field=models.ForeignKey(to='editorial.User'),
        ),
        migrations.AddField(
            model_name='asset',
            name='series_id',
            field=models.ForeignKey(to='editorial.Series'),
        ),
    ]

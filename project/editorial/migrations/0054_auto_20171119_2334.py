# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0053_auto_20171119_2125'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(help_text=b'Name of the assignment.')),
                ('text', models.TextField(help_text=b'Details of the assignment.')),
                ('creation_date', models.DateTimeField(help_text=b'Day assignment was created.', auto_now_add=True)),
                ('rate', models.CharField(help_text=b'Rate at which the assignment is being completed.', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Call',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Title of the call.', max_length=50)),
                ('text', models.TextField(help_text=b'Text of the call.')),
                ('creation_date', models.DateTimeField(help_text=b'Day/Time call was created.', auto_now_add=True)),
                ('expiration_date', models.DateTimeField(help_text=b'Day/Time call ends.', auto_now_add=True, null=True)),
                ('is_active', models.BooleanField(default=True, help_text=b'Is this call active?')),
                ('urgent', models.BooleanField(default=False, help_text=b'Is this call urgent?')),
                ('timeframe', models.CharField(help_text=b'What is the timeframe for responses?', max_length=100, null=True, blank=True)),
                ('status', models.CharField(help_text=b'Pitch status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Published', b'Published'), (b'Complete', b'Complete')])),
                ('organization', models.ForeignKey(help_text=b'Organization that is making this call.', to='editorial.Organization')),
                ('owner', models.ForeignKey(help_text=b'User that owns this call.', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pitch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(help_text=b'Title of the pitch.')),
                ('text', models.TextField(help_text=b'Text of the pitch.')),
                ('creation_date', models.DateTimeField(help_text=b'Day pitch was created.', auto_now_add=True)),
                ('status', models.CharField(help_text=b'Pitch status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitched', b'Pitched'), (b'Accepted', b'Accepted'), (b'Complete', b'Complete')])),
                ('exclusive', models.BooleanField(default=False, help_text=b'Is this pitch for an assignment exclusive to the recipient?')),
                ('contributor', models.ForeignKey(to='editorial.ContractorInfo')),
            ],
        ),
        migrations.AddField(
            model_name='organizationcontractorinfo',
            name='talent_pool',
            field=models.BooleanField(default=False, help_text=b'Is this contractor a trusted regular?'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='call',
            field=models.ManyToManyField(help_text=b'If this assignment is related to a call, which one?', to='editorial.Call', blank=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='contributor',
            field=models.ForeignKey(to='editorial.ContractorInfo'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='editor',
            field=models.ForeignKey(help_text=b'Editor responsible for this assignment.', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignment',
            name='facet',
            field=models.ForeignKey(blank=True, to='editorial.Facet', help_text=b'Which facet is this assignment related to?', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='organization',
            field=models.ForeignKey(help_text=b'Organization that owns this assignment.', to='editorial.Organization'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='pitch',
            field=models.ForeignKey(blank=True, to='editorial.Pitch', help_text=b'If this assignment is related to a pitch, which one?', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='story',
            field=models.ForeignKey(blank=True, to='editorial.Story', help_text=b'Which story is this assignment related to?', null=True),
        ),
    ]

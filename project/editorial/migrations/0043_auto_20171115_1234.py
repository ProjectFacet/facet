# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields
from django.conf import settings
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0042_auto_20171115_1207'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacetTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100, blank=True)),
                ('fields', django.contrib.postgres.fields.ArrayField(default=list, help_text=b'Fields used by this template.', size=None, base_field=models.CharField(max_length=50), blank=True)),
                ('creation_date', models.DateTimeField(help_text=b'When template was created.', auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('organization', models.ForeignKey(blank=True, to='editorial.Organization', null=True)),
                ('owner', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='facet',
            name='template',
            field=models.ForeignKey(default=None, to='editorial.FacetTemplate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='historicalfacet',
            name='template',
            field=models.ForeignKey(related_name='+', on_delete=django.db.models.deletion.DO_NOTHING, db_constraint=False, blank=True, to='editorial.FacetTemplate', null=True),
        ),
    ]

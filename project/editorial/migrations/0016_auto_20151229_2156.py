# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0015_auto_20151228_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='audiofacet',
            old_name='content',
            new_name='af_content',
        ),
        migrations.RenameField(
            model_name='historicalaudiofacet',
            old_name='content',
            new_name='af_content',
        ),
        migrations.RenameField(
            model_name='historicalprintfacet',
            old_name='content',
            new_name='pf_content',
        ),
        migrations.RenameField(
            model_name='historicalvideofacet',
            old_name='content',
            new_name='vf_content',
        ),
        migrations.RenameField(
            model_name='historicalwebfacet',
            old_name='content',
            new_name='wf_content',
        ),
        migrations.RenameField(
            model_name='printfacet',
            old_name='content',
            new_name='pf_content',
        ),
        migrations.RenameField(
            model_name='videofacet',
            old_name='content',
            new_name='vf_content',
        ),
        migrations.RenameField(
            model_name='webfacet',
            old_name='content',
            new_name='wf_content',
        ),
    ]

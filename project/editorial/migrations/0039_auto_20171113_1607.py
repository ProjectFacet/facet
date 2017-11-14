# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0038_facetcopydetail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='facet',
            old_name='edit_notes',
            new_name='edit_note',
        ),
        migrations.RenameField(
            model_name='facet',
            old_name='update_notes',
            new_name='update_note',
        ),
        migrations.RenameField(
            model_name='historicalfacet',
            old_name='edit_notes',
            new_name='edit_note',
        ),
        migrations.RenameField(
            model_name='historicalfacet',
            old_name='update_notes',
            new_name='update_note',
        ),
        migrations.AddField(
            model_name='facet',
            name='description',
            field=models.TextField(help_text=b'Description of the facet.', blank=True),
        ),
        migrations.AddField(
            model_name='historicalfacet',
            name='description',
            field=models.TextField(help_text=b'Description of the facet.', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0034_auto_20160113_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofacet',
            name='status',
            field=models.CharField(help_text=b'Audiofacet status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitch', b'Pitch'), (b'In Progress', b'In Progress'), (b'Edit', b'Edit'), (b'Revision', b'Revision'), (b'Needs Review', b'Needs Review'), (b'Ready', b'Ready')]),
        ),
        migrations.AlterField(
            model_name='historicalaudiofacet',
            name='status',
            field=models.CharField(help_text=b'Audiofacet status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitch', b'Pitch'), (b'In Progress', b'In Progress'), (b'Edit', b'Edit'), (b'Revision', b'Revision'), (b'Needs Review', b'Needs Review'), (b'Ready', b'Ready')]),
        ),
        migrations.AlterField(
            model_name='historicalprintfacet',
            name='status',
            field=models.CharField(help_text=b'Printfacet status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitch', b'Pitch'), (b'In Progress', b'In Progress'), (b'Edit', b'Edit'), (b'Revision', b'Revision'), (b'Needs Review', b'Needs Review'), (b'Ready', b'Ready')]),
        ),
        migrations.AlterField(
            model_name='historicalvideofacet',
            name='status',
            field=models.CharField(help_text=b'Videofacet status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitch', b'Pitch'), (b'In Progress', b'In Progress'), (b'Edit', b'Edit'), (b'Revision', b'Revision'), (b'Needs Review', b'Needs Review'), (b'Ready', b'Ready')]),
        ),
        migrations.AlterField(
            model_name='historicalwebfacet',
            name='status',
            field=models.CharField(help_text=b'WebFacet status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitch', b'Pitch'), (b'In Progress', b'In Progress'), (b'Edit', b'Edit'), (b'Revision', b'Revision'), (b'Needs Review', b'Needs Review'), (b'Ready', b'Ready')]),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='status',
            field=models.CharField(help_text=b'Printfacet status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitch', b'Pitch'), (b'In Progress', b'In Progress'), (b'Edit', b'Edit'), (b'Revision', b'Revision'), (b'Needs Review', b'Needs Review'), (b'Ready', b'Ready')]),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='status',
            field=models.CharField(help_text=b'Videofacet status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitch', b'Pitch'), (b'In Progress', b'In Progress'), (b'Edit', b'Edit'), (b'Revision', b'Revision'), (b'Needs Review', b'Needs Review'), (b'Ready', b'Ready')]),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='status',
            field=models.CharField(help_text=b'WebFacet status choice.', max_length=25, choices=[(b'Draft', b'Draft'), (b'Pitch', b'Pitch'), (b'In Progress', b'In Progress'), (b'Edit', b'Edit'), (b'Revision', b'Revision'), (b'Needs Review', b'Needs Review'), (b'Ready', b'Ready')]),
        ),
    ]

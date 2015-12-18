# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0005_auto_20151216_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalprintfacet',
            name='status',
            field=models.CharField(default='draft', help_text=b'Printfacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='printfacet',
            name='status',
            field=models.CharField(default='draft', help_text=b'Printfacet status choice.', max_length=25, choices=[(b'DRFT', b'Draft'), (b'PT', b'Pitch'), (b'IP', b'In Progress'), (b'EDT', b'Edit'), (b'RVN', b'Revision'), (b'RDY', b'Ready')]),
            preserve_default=False,
        ),
    ]

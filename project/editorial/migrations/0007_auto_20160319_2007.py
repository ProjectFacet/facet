# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0006_auto_20160319_1837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentasset',
            name='doc_type',
            field=models.CharField(help_text=b'What kind of image.', max_length=20, choices=[(b'PDF', b'Adobe PDF'), (b'WORD DOC', b'Word Doc'), (b'TEXT', b'Text File'), (b'COMMA SEPARATED', b'Comma Separated'), (b'EXCEL', b'Excel File'), (b'OTHER', b'Other')]),
        ),
    ]

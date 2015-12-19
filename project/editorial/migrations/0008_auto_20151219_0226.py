# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0007_auto_20151219_0224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofacet',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of edit discussion for the audiofacet.', null=True),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of edit discussion for the printfacet.', null=True),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'ID of edit discussion for the videofacet.', null=True),
        ),
    ]

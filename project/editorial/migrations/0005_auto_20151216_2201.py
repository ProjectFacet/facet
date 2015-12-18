# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0004_auto_20151216_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webfacet',
            name='assets',
            field=models.ManyToManyField(to='editorial.Asset', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='discussion',
            field=models.ForeignKey(blank=True, to='editorial.Discussion', help_text=b'Id of edit discussion for the webfacet.', null=True),
        ),
    ]

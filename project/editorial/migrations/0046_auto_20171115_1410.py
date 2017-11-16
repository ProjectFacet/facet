# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0045_auto_20171115_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facet',
            name='content_license',
            field=models.ForeignKey(related_name='facetlicense', blank=True, to='editorial.ContentLicense', null=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0043_auto_20171115_1234'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='facettemplate',
            options={'ordering': ['id']},
        ),
        migrations.AlterUniqueTogether(
            name='facettemplate',
            unique_together=set([('name', 'organization')]),
        ),
    ]

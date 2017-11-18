# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0049_auto_20171116_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facet',
            name='story',
            field=models.ForeignKey(related_name='storyfacet', to='editorial.Story'),
        ),
    ]

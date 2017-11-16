# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0046_auto_20171115_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='facet',
            name='producer',
            field=models.ForeignKey(related_name='facetproducer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]

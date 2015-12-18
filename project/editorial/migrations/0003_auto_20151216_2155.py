# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0002_auto_20151216_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webfacet',
            name='contributors',
            field=models.ManyToManyField(help_text=b'Users that contributed to a facet. Used to associate multiple users to a facet.', to=settings.AUTH_USER_MODEL, through='editorial.WebFacetContributor', blank=True),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='credit',
            field=models.ManyToManyField(help_text=b'The full user name(s) to be listed as the credit for the facet.', related_name='webfacetcredit', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]

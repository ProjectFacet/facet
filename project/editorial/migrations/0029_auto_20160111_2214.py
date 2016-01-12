# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0028_auto_20160111_1551'),
    ]

    operations = [
        migrations.AddField(
            model_name='networknote',
            name='network',
            field=models.ForeignKey(related_name='networknote_network', default=1, to='editorial.Network'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organizationnote',
            name='organization',
            field=models.ForeignKey(related_name='orgnote_org', default=3, to='editorial.Organization'),
            preserve_default=False,
        ),
    ]

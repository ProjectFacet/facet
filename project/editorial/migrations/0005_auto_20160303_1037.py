# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0004_auto_20160227_1641'),
    ]

    operations = [
        migrations.AddField(
            model_name='seriesnote',
            name='organization',
            field=models.ForeignKey(related_name='seriesnote_org', default=3, to='editorial.Organization'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='storynote',
            name='organization',
            field=models.ForeignKey(related_name='storynote_org', default=3, to='editorial.Organization'),
            preserve_default=False,
        ),
    ]

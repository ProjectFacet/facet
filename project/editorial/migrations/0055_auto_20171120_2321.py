# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0054_auto_20171119_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audioasset',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='documentasset',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='imageasset',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='simpleaudio',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='simpledocument',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='simpleimage',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='simplevideo',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='videoasset',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', null=True),
        ),
    ]

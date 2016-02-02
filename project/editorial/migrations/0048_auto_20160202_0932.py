# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0047_auto_20160201_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageasset',
            name='organization',
            field=models.ForeignKey(related_name='image_asset_organization', default=3, to='editorial.Organization'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imageasset',
            name='original',
            field=models.BooleanField(default=True, help_text=b'This content originally belonged to this organization.'),
        ),
        migrations.AlterField(
            model_name='imageasset',
            name='owner',
            field=models.ForeignKey(related_name='image_asset_owner', to=settings.AUTH_USER_MODEL),
        ),
    ]

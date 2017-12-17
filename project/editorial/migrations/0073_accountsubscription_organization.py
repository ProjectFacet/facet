# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0072_accountsubscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountsubscription',
            name='organization',
            field=models.ForeignKey(blank=True, to='editorial.Organization', help_text=b'Organization associated with this subscription if Org subscription type.', null=True),
        ),
    ]

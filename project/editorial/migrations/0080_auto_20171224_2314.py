# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0079_auto_20171224_2308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='editor',
            field=models.ForeignKey(help_text=b'Editor responsible for this assignment.', to='editorial.TalentEditorProfile'),
        ),
        migrations.AlterField(
            model_name='call',
            name='owner',
            field=models.ForeignKey(help_text=b'Editor that owns this call.', to='editorial.TalentEditorProfile'),
        ),
        migrations.AlterField(
            model_name='pitch',
            name='recipient',
            field=models.ForeignKey(help_text=b'To whom is this pitch directed?', to='editorial.TalentEditorProfile'),
        ),
    ]

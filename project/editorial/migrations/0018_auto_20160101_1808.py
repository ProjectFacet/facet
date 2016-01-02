# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0017_story_original_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='audiofacet',
            name='story',
            field=models.ForeignKey(related_name='audiofacetstory', to='editorial.Story'),
        ),
        migrations.AlterField(
            model_name='printfacet',
            name='story',
            field=models.ForeignKey(related_name='printfacetstory', to='editorial.Story'),
        ),
        migrations.AlterField(
            model_name='videofacet',
            name='story',
            field=models.ForeignKey(related_name='videofacetstory', to='editorial.Story'),
        ),
        migrations.AlterField(
            model_name='webfacet',
            name='story',
            field=models.ForeignKey(related_name='webfacetstory', to='editorial.Story'),
        ),
    ]

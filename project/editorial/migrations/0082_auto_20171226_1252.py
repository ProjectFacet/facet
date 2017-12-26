# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0081_auto_20171226_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.ManyToManyField(to='editorial.Note', blank=True),
        ),
        migrations.AddField(
            model_name='network',
            name='notes',
            field=models.ManyToManyField(to='editorial.Note', blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='notes',
            field=models.ManyToManyField(to='editorial.Note', blank=True),
        ),
        migrations.AddField(
            model_name='project',
            name='notes',
            field=models.ManyToManyField(to='editorial.Note', blank=True),
        ),
        migrations.AddField(
            model_name='series',
            name='notes',
            field=models.ManyToManyField(to='editorial.Note', blank=True),
        ),
        migrations.AddField(
            model_name='story',
            name='notes',
            field=models.ManyToManyField(to='editorial.Note', blank=True),
        ),
        migrations.AddField(
            model_name='task',
            name='notes',
            field=models.ManyToManyField(to='editorial.Note', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='notes',
            field=models.ManyToManyField(to='editorial.Note', blank=True),
        ),
    ]

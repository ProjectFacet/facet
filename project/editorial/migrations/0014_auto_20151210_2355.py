# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0013_auto_20151210_2256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['credit_name'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
        migrations.AddField(
            model_name='series',
            name='sensitivity',
            field=models.BooleanField(default=False, help_text=b'Is a story sensitive, for limited viewing?'),
        ),
        migrations.AlterField(
            model_name='story',
            name='collaborate_with',
            field=models.ManyToManyField(help_text=b'Network ids that a story is open to collaboration with.', related_name='story_collaborated_with_network', to='editorial.Network', blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='series_id',
            field=models.ForeignKey(to='editorial.Series', blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='share_with',
            field=models.ManyToManyField(help_text=b'Network ids that a story is shared with.', related_name='story_shared_with_network', to='editorial.Network', blank=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='team',
            field=models.ManyToManyField(help_text=b'User contributing to the story.', related_name='story_team_member', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]

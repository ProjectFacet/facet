# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0078_auto_20171218_1301'),
    ]

    operations = [
        migrations.CreateModel(
            name='TalentEditorProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public', models.BooleanField(default=False, help_text=b'Is this talent editor publicly listed?')),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='public',
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(help_text=b'Type of user.', max_length=25, choices=[(b'Admin', b'Admin'), (b'Editor', b'Editor'), (b'Staff', b'Staff'), (b'Other', b'Other')]),
        ),
        migrations.AddField(
            model_name='talenteditorprofile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]

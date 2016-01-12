# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0029_auto_20160111_2214'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='discussion',
            field=models.ForeignKey(related_name='network_discussion', blank=True, to='editorial.Discussion', help_text=b'Id of discussion for a network.', null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='discussion',
            field=models.ForeignKey(related_name='organization_discussion', blank=True, to='editorial.Discussion', help_text=b'Id of discussion for an organization.', null=True),
        ),
        migrations.AlterField(
            model_name='discussion',
            name='discussion_type',
            field=models.CharField(help_text=b'What kind of discussion is it.', max_length=25, choices=[(b'ORG', b'Organization Conversation'), (b'NET', b'Network Conversation'), (b'PRI', b'Private Conversation'), (b'SER', b'Series Conversation'), (b'STO', b'Story Conversation'), (b'WF', b'WebFacet Conversation'), (b'PF', b'PrintFacet Conversation'), (b'AF', b'AudioFacet Conversation'), (b'VF', b'VideoFacet Conversation')]),
        ),
    ]

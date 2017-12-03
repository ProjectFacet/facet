# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0060_auto_20171202_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractorProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('resume', models.FileField(help_text=b'PDF of contractor resume.', upload_to=b'resumes/%Y/%m/%d', blank=True)),
                ('address', models.TextField(help_text=b'Mailing address.', blank=True)),
                ('availability', models.TextField(help_text=b'Notes on when a contractor is available or not.', blank=True)),
                ('current_location', models.TextField(help_text=b"Contractor's specific location.", blank=True)),
                ('gear', models.TextField(help_text=b'Gear that a contractor has access to and skills for.', blank=True)),
                ('portfolio_link1', models.URLField(help_text=b'Link to portfolio item.', max_length=500, null=True, blank=True)),
                ('portfolio_link2', models.URLField(help_text=b'Link to portfolio item.', max_length=500, null=True, blank=True)),
                ('portfolio_link3', models.URLField(help_text=b'Link to portfolio item.', max_length=500, null=True, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='contractorinfo',
            name='user',
        ),
        migrations.RemoveField(
            model_name='organizationcontractorinfo',
            name='contractor_info',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='contributor',
            field=models.ForeignKey(to='editorial.ContractorProfile'),
        ),
        migrations.AlterField(
            model_name='pitch',
            name='contributor',
            field=models.ForeignKey(to='editorial.ContractorProfile'),
        ),
        migrations.DeleteModel(
            name='ContractorInfo',
        ),
        migrations.AddField(
            model_name='organizationcontractorinfo',
            name='contractor',
            field=models.ForeignKey(default=1, to='editorial.ContractorProfile'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0061_auto_20171202_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrganizationContractorAffiliation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('w9_on_file', models.BooleanField(default=False, help_text=b'Does the organization have a W9 on file.')),
                ('rates', models.TextField(help_text=b'The rates the contractor is paid by the org.', blank=True)),
                ('strengths', models.TextField(help_text=b'Internal notes on strengths of the contractor.', blank=True)),
                ('conflicts', models.TextField(help_text=b'Any conflicts of interest the contractor has.', blank=True)),
                ('editor_notes', models.TextField(help_text=b'Any notes for editors on things to know when working with this contractor.', blank=True)),
                ('talent_pool', models.BooleanField(default=False, help_text=b'Is this contractor a trusted regular?')),
                ('status', models.BooleanField(default=True, help_text=b'Is this contractor currently working for the organization?')),
                ('contractor', models.ForeignKey(to='editorial.ContractorProfile')),
                ('organization', models.ForeignKey(to='editorial.Organization')),
            ],
        ),
        migrations.RemoveField(
            model_name='organizationcontractorinfo',
            name='contractor',
        ),
        migrations.RemoveField(
            model_name='organizationcontractorinfo',
            name='organization',
        ),
        migrations.DeleteModel(
            name='OrganizationContractorInfo',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editorial', '0037_auto_20171113_1058'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacetCopyDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('copy_date', models.DateTimeField(help_text=b'Datetime when copy was made.', auto_now_add=True)),
                ('original_facet', models.ForeignKey(related_name='original_facet_detail', to='editorial.Facet', help_text=b'Original copy of the facet.')),
                ('original_org', models.ForeignKey(related_name='original_facet_organization', to='editorial.Organization', help_text=b'Organization that originally created the content.')),
                ('partner', models.ForeignKey(related_name='facet_copying_organization', to='editorial.Organization', help_text=b'Organization that made the copy.')),
                ('partner_facet', models.ForeignKey(related_name='facet_copy', to='editorial.Facet', help_text=b'The new version of the facet saved by the partner organization.')),
            ],
        ),
    ]

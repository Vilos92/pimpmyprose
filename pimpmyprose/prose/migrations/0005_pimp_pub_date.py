# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('prose', '0004_pimp_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='pimp',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2015, 3, 1, 5, 24, 34, 967000, tzinfo=utc), verbose_name=b'date published'),
            preserve_default=False,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('prose', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='prose',
            name='user',
            field=models.ForeignKey(default=100, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='website',
            field=models.URLField(default=150, blank=True),
            preserve_default=False,
        ),
    ]

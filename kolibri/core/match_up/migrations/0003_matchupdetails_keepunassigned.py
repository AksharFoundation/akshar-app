# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-04 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match_up', '0002_auto_20211129_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='matchupdetails',
            name='keepUnassigned',
            field=models.BooleanField(default=False),
        ),
    ]
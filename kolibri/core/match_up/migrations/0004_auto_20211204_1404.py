# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-12-04 08:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('match_up', '0003_matchupdetails_keepunassigned'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchupdetails',
            name='keepUnassigned',
            field=models.NullBooleanField(default=False),
        ),
    ]
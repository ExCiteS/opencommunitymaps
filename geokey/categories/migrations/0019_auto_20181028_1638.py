# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-28 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0018_historicalcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lookupvalue',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='multiplelookupvalue',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='lookupvalue',
            name='order',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='multiplelookupvalue',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-10-28 15:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('socialaccount', '0003_extra_data_default_dict'),
        ('projects', '0007_auto_20160122_1409'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialInteraction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('text_to_post', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socialinteractions', to='projects.Project')),
                ('socialaccount', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='socialinteractions', to='socialaccount.SocialAccount')),
            ],
        ),
    ]

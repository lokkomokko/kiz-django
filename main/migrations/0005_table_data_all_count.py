# Generated by Django 2.0 on 2017-12-31 14:03

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='data_all_count',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]

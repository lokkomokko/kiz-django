# Generated by Django 2.0 on 2017-12-26 11:52

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0016_auto_20171226_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='med',
            name='pub_date',
            field=models.DateField(default=datetime.datetime(2017, 12, 26, 11, 52, 33, 290236, tzinfo=utc)),
        ),
    ]

# Generated by Django 2.0 on 2018-01-01 23:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20171231_1411'),
    ]

    operations = [
        migrations.AlterField(
            model_name='med',
            name='date_1',
            field=models.DateField(default=datetime.datetime(2018, 1, 1, 23, 39, 59, 212202, tzinfo=utc), help_text='Период болезни', verbose_name='С '),
        ),
        migrations.AlterField(
            model_name='med',
            name='date_2',
            field=models.DateField(default=datetime.datetime(2018, 1, 1, 23, 39, 59, 212228, tzinfo=utc), verbose_name='По'),
        ),
    ]

# Generated by Django 2.0 on 2017-12-23 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20171223_2019'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='med',
            name='adults',
        ),
        migrations.AddField(
            model_name='med',
            name='adult',
            field=models.IntegerField(default=30, verbose_name='Возраст'),
            preserve_default=False,
        ),
    ]
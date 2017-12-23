# Generated by Django 2.0 on 2017-12-23 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_med_days'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='med',
            name='sex',
        ),
        migrations.AddField(
            model_name='med',
            name='sexxxx',
            field=models.CharField(choices=[('муж', 'муж'), ('жен', 'жен')], default='муж', max_length=5, verbose_name='Пол'),
        ),
    ]
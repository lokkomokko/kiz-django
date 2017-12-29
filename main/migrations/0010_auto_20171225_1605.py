# Generated by Django 2.0 on 2017-12-25 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_sicksundergroup_group_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='sickssingle',
            name='under_group_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.SicksUndergroup', verbose_name='Подгруппа'),
        ),
        migrations.AlterField(
            model_name='sickssingle',
            name='group_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Sicks', verbose_name='Группа'),
        ),
    ]
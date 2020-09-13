# Generated by Django 2.2.6 on 2020-09-13 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20200913_1226'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='is_cr',
            field=models.BooleanField(default=False, verbose_name='CR'),
        ),
        migrations.AlterField(
            model_name='student',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.Section', verbose_name='Section'),
        ),
    ]

# Generated by Django 2.2.2 on 2020-01-22 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_depature_flight'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='depature',
            name='seats',
        ),
        migrations.AddField(
            model_name='seat',
            name='depature',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='mainapp.Depature'),
        ),
    ]

# Generated by Django 4.1.3 on 2022-11-15 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('measurement', '0004_alter_sensor_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
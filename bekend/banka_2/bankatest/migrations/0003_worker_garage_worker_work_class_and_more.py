# Generated by Django 5.0.4 on 2024-06-10 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankatest', '0002_vehicle_brand_vehicle_fuel_consumption_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='garage',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='worker',
            name='work_class',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='worker',
            name='work_experience',
            field=models.IntegerField(default=0),
        ),
    ]

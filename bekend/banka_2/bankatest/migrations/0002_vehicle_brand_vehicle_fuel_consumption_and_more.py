# Generated by Django 5.0.4 on 2024-06-10 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankatest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='brand',
            field=models.CharField(default='0', max_length=50),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='fuel_consumption',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='manufacturer',
            field=models.CharField(default='0', max_length=50),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='payload_capacity',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='state_number',
            field=models.TextField(default='0'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='trailer_length',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='transportation_cost_per_km',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
    ]

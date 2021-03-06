# Generated by Django 2.2.7 on 2019-11-05 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='protocol',
            field=models.CharField(choices=[('http', 'http'), ('https', 'https')], default='http', max_length=5),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('cancelled', 'cancelled'), ('confirmed', 'confirmed')], default='pending', max_length=10),
        ),
    ]

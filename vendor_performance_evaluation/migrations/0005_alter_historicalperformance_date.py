# Generated by Django 4.2.7 on 2023-12-10 07:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_performance_evaluation', '0004_alter_historicalperformance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='date',
            field=models.DateField(default=datetime.datetime(2023, 12, 10, 7, 51, 16, 537371, tzinfo=datetime.timezone.utc)),
        ),
    ]
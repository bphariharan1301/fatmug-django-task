# Generated by Django 4.2.7 on 2023-12-10 07:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_performance_evaluation', '0002_alter_historicalperformance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalperformance',
            name='date',
            field=models.DateField(default=datetime.date(2023, 12, 10)),
        ),
    ]
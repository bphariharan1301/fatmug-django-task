# Generated by Django 4.2.7 on 2023-12-10 07:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_profile', '0003_alter_historicalperformance_vendor'),
    ]

    operations = [
        migrations.DeleteModel(
            name='HistoricalPerformance',
        ),
    ]

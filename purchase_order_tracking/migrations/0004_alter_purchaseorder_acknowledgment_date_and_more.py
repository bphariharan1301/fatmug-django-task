# Generated by Django 4.2.7 on 2023-12-06 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase_order_tracking', '0003_alter_purchaseorder_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='acknowledgment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='delivery_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='issue_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='order_date',
            field=models.DateField(),
        ),
    ]

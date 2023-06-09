# Generated by Django 4.2 on 2023-05-19 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_order_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SHIPPING', 'Shipping'), ('DELIVERED', 'Delivered'), ('CANCELED', 'Canceled'), ('REFUNDED', 'Refunded')], default='PENDING', max_length=10),
        ),
    ]

# Generated by Django 4.2 on 2023-05-16 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_apartment_no_order_building_no_order_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='city',
            field=models.TextField(null=True),
        ),
    ]

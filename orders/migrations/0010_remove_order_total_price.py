# Generated by Django 4.2.4 on 2023-09-08 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_remove_orderproduct_discount_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_price',
        ),
    ]
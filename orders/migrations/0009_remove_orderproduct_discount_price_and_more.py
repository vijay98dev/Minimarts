# Generated by Django 4.2.4 on 2023-09-08 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_orderproduct_discount_price_orderproduct_sub_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderproduct',
            name='discount_price',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='tax',
        ),
        migrations.RemoveField(
            model_name='orderproduct',
            name='total_price',
        ),
        migrations.AddField(
            model_name='order',
            name='discount_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='total',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='order',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
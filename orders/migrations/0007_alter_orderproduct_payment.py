# Generated by Django 4.2.4 on 2023-09-02 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_remove_order_payment_payment_order_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='payment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment'),
        ),
    ]

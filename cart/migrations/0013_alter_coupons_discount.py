# Generated by Django 4.2.4 on 2023-09-06 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0012_coupons_usercoupons_cart_coupon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupons',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]

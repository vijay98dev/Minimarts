# Generated by Django 4.2.4 on 2023-08-28 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_productsize_product_size'),
        ('cart', '0005_wishlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitems',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productsize'),
        ),
    ]
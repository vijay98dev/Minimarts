# Generated by Django 4.2.4 on 2023-08-29 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_productsize_product_size'),
        ('cart', '0010_alter_cartitems_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlist',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productsize'),
        ),
    ]

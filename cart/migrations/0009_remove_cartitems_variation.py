# Generated by Django 4.2.4 on 2023-08-28 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_cartitems_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='variation',
        ),
    ]

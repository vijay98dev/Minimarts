# Generated by Django 4.2.4 on 2023-08-31 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_userprofile_first_name_userprofile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_image',
            field=models.ImageField(default='admin/assets/img/avatars/5.png', null=True, upload_to='photo/profile-image'),
        ),
    ]

# Generated by Django 4.2.3 on 2023-08-03 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_profile_address_line_2_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='country',
            new_name='full_name',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='first_name',
            new_name='pincode',
        ),
    ]
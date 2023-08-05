# Generated by Django 4.2.3 on 2023-08-03 14:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='country',
            new_name='full_name',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='first_name',
            new_name='pincode',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address_line_2',
        ),
        migrations.RemoveField(
            model_name='order',
            name='last_name',
        ),
    ]
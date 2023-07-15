# Generated by Django 4.2.3 on 2023-07-15 05:02

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='account',
            name='mobile',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='mobile number'),
        ),
    ]

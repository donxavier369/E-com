# Generated by Django 4.2.3 on 2023-08-13 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_rename_order_id_razorpay_order_provider_order_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
    ]

# Generated by Django 4.2.13 on 2024-07-09 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("restaurant", "0008_order_time_slot_alter_order_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="order",
            name="time_slot",
        ),
    ]

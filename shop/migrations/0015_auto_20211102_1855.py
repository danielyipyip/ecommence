# Generated by Django 2.1.15 on 2021-11-02 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20211102_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderitems',
            field=models.ManyToManyField(to='shop.OrderItem'),
        ),
    ]
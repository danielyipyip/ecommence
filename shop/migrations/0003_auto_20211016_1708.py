# Generated by Django 2.1.5 on 2021-10-16 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_auto_20211016_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderDate',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

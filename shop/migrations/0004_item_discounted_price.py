# Generated by Django 2.1.5 on 2021-10-17 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20211016_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='discounted_price',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=20),
            preserve_default=False,
        ),
    ]

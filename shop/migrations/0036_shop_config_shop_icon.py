# Generated by Django 3.2.9 on 2021-12-03 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0035_auto_20211128_1650'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop_config',
            name='shop_icon',
            field=models.ImageField(blank=True, null=True, upload_to='contact_us'),
        ),
    ]

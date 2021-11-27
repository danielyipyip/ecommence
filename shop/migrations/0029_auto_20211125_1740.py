# Generated by Django 2.1.15 on 2021-11-25 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0028_shop_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop_config',
            name='facebook',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop_config',
            name='google_play',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop_config',
            name='instagram',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shop_config',
            name='paypal_account',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='shop_config',
            name='twitter',
            field=models.URLField(blank=True, null=True),
        ),
    ]
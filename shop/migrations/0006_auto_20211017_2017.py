# Generated by Django 2.1.5 on 2021-10-17 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20211017_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(blank=True, choices=[('new', 'new-arrival'), ('best', 'best-seller'), ('recom', 'recommended'), ('sales', 'sales')], max_length=20, null=True),
        ),
    ]

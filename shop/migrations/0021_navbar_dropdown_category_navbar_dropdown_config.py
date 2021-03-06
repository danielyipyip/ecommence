# Generated by Django 2.1.15 on 2021-11-11 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_auto_20211110_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='navbar_dropdown_category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(choices=[('tee', 't-shirt'), ('shirt', 'shirt'), ('jean', 'jeans'), ('dress', 'dresses'), ('trousers', 'trousers'), ('jacket', 'coats and jackets')], max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='navbar_dropdown_config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('categories', models.ManyToManyField(to='shop.navbar_dropdown_category')),
            ],
        ),
    ]

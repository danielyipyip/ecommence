# Generated by Django 2.1.5 on 2021-10-25 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20211019_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, height_field=600, upload_to='product_images', width_field=600),
        ),
        migrations.AlterField(
            model_name='item',
            name='product_type',
            field=models.CharField(choices=[('tee', 't-shirt'), ('shirt', 'shirt'), ('jean', 'jeans'), ('dress', 'dresses'), ('trousers', 'trousers'), ('jacket', 'coats and jackets')], max_length=20),
        ),
    ]
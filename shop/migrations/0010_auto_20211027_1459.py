# Generated by Django 2.1.5 on 2021-10-27 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0009_auto_20211025_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, default='C:/Users/daniel/Workspace/ecommerce/media/product_images/white_tshirt.jpg', height_field='image_height', upload_to='product_images', width_field='image_width'),
        ),
    ]
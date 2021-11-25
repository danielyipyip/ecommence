# Generated by Django 2.1.15 on 2021-11-25 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0029_auto_20211125_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact_us_config',
            name='portal1_image',
            field=models.ImageField(blank=True, null=True, upload_to='contact_us'),
        ),
        migrations.AddField(
            model_name='contact_us_config',
            name='portal1_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact_us_config',
            name='portal2_image',
            field=models.ImageField(blank=True, null=True, upload_to='contact_us'),
        ),
        migrations.AddField(
            model_name='contact_us_config',
            name='portal2_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='contact_us_config',
            name='portal3_image',
            field=models.ImageField(blank=True, null=True, upload_to='contact_us'),
        ),
        migrations.AddField(
            model_name='contact_us_config',
            name='portal3_link',
            field=models.URLField(blank=True, null=True),
        ),
    ]

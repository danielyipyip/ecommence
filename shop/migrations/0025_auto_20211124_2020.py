# Generated by Django 2.1.15 on 2021-11-24 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0024_type_choice_product_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='contact_us_config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='C:\\Users\\daniel\\Workspace\\ecommerce\\media\\contact_us\\shirt1_square.jpg', upload_to='contact_us')),
                ('title', models.CharField(max_length=100)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='page_link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('cover_image', models.ImageField(upload_to='contact_us')),
                ('link', models.URLField()),
                ('description', models.TextField()),
                ('contact_us', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.contact_us_config')),
            ],
        ),
        migrations.AlterField(
            model_name='type_choice',
            name='product_gender',
            field=models.CharField(choices=[('Woman', 'Woman'), ('Man', 'Man'), ('Both', 'Both'), ('Kid', 'Kids'), ('All', 'All')], default='woman', max_length=20),
        ),
    ]

# Generated by Django 5.1.6 on 2025-02-17 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candle', '0002_alter_candle_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='gallery/')),
            ],
        ),
    ]

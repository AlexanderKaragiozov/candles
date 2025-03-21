# Generated by Django 5.1.6 on 2025-03-08 17:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candle', '0015_candleorder_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='candle',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='candle',
            name='monthly',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='candleorder',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2025, 3, 9, 17, 48, 42, 154375, tzinfo=datetime.timezone.utc)),
        ),
    ]

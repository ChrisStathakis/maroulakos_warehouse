# Generated by Django 3.0.1 on 2021-04-26 15:05

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0011_auto_20210422_0729'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 26, 15, 4, 59, 603638, tzinfo=utc), verbose_name='Ημερομηνία'),
        ),
    ]

# Generated by Django 3.0.1 on 2020-03-28 14:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0018_auto_20200328_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 28, 14, 10, 52, 636704, tzinfo=utc), verbose_name='Ημερομηνία'),
        ),
    ]

# Generated by Django 3.0.4 on 2020-04-13 07:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0018_auto_20200412_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 13, 7, 17, 53, 245212, tzinfo=utc), verbose_name='Ημερομηνία'),
        ),
    ]

# Generated by Django 3.0.4 on 2020-04-03 12:23

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('costumers', '0005_auto_20200403_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentinvoice',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 3, 12, 23, 9, 518216, tzinfo=utc), verbose_name='Ημερομηνία'),
        ),
    ]

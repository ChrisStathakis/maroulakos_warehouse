# Generated by Django 3.0.1 on 2021-01-25 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_auto_20210123_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='order_type',
            field=models.CharField(choices=[('a', 'Τιμολογιο'), ('b', 'Δελτιο Αποστολης'), ('c', 'Εισαγωγη στην Αποθηκη'), ('d', 'Εξαγωγη απο την Αποθηκη')], default='a', max_length=1, verbose_name='Είδος Παραστατικού'),
        ),
    ]

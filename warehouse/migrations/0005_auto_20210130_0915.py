# Generated by Django 3.0.1 on 2021-01-30 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_auto_20210125_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoiceitem',
            name='order_code',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Κωδικος Τιμολογιου'),
        ),
    ]
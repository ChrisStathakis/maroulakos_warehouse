# Generated by Django 3.0.1 on 2021-01-25 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0003_auto_20210125_0702'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicetransformation',
            name='cost',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=17, verbose_name='Κοστολογηση'),
        ),
        migrations.AlterField(
            model_name='invoicetransformation',
            name='value',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=17, verbose_name='Αξια'),
        ),
        migrations.AlterField(
            model_name='invoicetransformationingredient',
            name='cost',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=17),
        ),
        migrations.AlterField(
            model_name='invoicetransformationingredient',
            name='total_cost',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=17),
        ),
        migrations.AlterField(
            model_name='invoicetransformationitem',
            name='total_cost',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=17),
        ),
        migrations.AlterField(
            model_name='invoicetransformationitem',
            name='total_value',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=17),
        ),
        migrations.AlterField(
            model_name='warehousemovementinvoiceitem',
            name='total_value',
            field=models.DecimalField(decimal_places=3, max_digits=17, verbose_name='Συνολική Αξια'),
        ),
        migrations.AlterField(
            model_name='warehousemovementinvoiceitem',
            name='value',
            field=models.DecimalField(decimal_places=3, max_digits=17, verbose_name='Αξια'),
        ),
    ]

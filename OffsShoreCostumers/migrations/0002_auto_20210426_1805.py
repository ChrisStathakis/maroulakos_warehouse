# Generated by Django 3.0.1 on 2021-04-26 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OffsShoreCostumers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offsshorecompany',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=30, verbose_name='Υπόλοιπο'),
        ),
        migrations.AlterField(
            model_name='offsshorecompanycostumer',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=30, verbose_name='Υπόλοιπο'),
        ),
    ]

# Generated by Django 2.2.4 on 2021-01-29 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0004_auto_20210125_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='payment_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='project_settings.PaymentMethod', verbose_name='Τροπος Πληρωμης'),
        ),
    ]

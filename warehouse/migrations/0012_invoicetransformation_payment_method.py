# Generated by Django 3.0.1 on 2020-03-28 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_settings', '0001_initial'),
        ('warehouse', '0011_auto_20200328_0737'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoicetransformation',
            name='payment_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='project_settings.PaymentMethod'),
        ),
    ]
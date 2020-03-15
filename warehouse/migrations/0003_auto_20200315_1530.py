# Generated by Django 3.0.1 on 2020-03-15 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0003_product_taxes_modifier'),
        ('warehouse', '0002_auto_20200314_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='order_type',
            field=models.CharField(choices=[('a', 'Τιμολογιο'), ('b', 'Δελτιο Αποστολης'), ('c', 'Εισαγωγη στην Αποθηκη'), ('d', 'Εξαγωγη απο την Αποθηκη')], default='a', max_length=1),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='storage_invoices', to='catalogue.ProductStorage'),
        ),
    ]

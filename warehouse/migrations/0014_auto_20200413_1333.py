# Generated by Django 3.0.4 on 2020-04-13 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20200405_1349'),
        ('warehouse', '0013_warehousemovementinvoiceitem_warehousemovementsinvoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehousemovementinvoiceitem',
            name='invoice',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='warehouse.WarehouseMovementsInvoice', verbose_name='Παραστατικο'),
        ),
        migrations.AlterField(
            model_name='warehousemovementinvoiceitem',
            name='storage',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='catalogue.ProductStorage', verbose_name='Αποθηκη'),
        ),
        migrations.AlterField(
            model_name='warehousemovementsinvoice',
            name='order_type',
            field=models.CharField(choices=[('a', 'Παραστατικο Εισαγωγής'), ('b', 'Παραστατικο Εξαγωγης'), ('c', 'Φυρα')], max_length=1, verbose_name='Ειδος'),
        ),
    ]

# Generated by Django 2.2 on 2020-03-27 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20200318_0711'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Κατασταση'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(blank=True, null=True, to='catalogue.Category', verbose_name='Κατηγοριες'),
        ),
        migrations.AlterField(
            model_name='product',
            name='order_sku',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Κωδικος Τιμολογιου'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_class',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='catalogue.ProductClass', verbose_name='Ειδος'),
        ),
        migrations.AlterField(
            model_name='product',
            name='safe_stock',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Ασφαλη Αποθεμα'),
        ),
        migrations.AlterField(
            model_name='product',
            name='sku',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='MPN'),
        ),
        migrations.AlterField(
            model_name='product',
            name='unit',
            field=models.CharField(blank=True, choices=[('a', 'Τεμάχιο'), ('b', 'Κιβώτιο'), ('c', 'Κιλό')], default='1', max_length=1, null=True, verbose_name='ΜΜ'),
        ),
    ]
# Generated by Django 3.0.4 on 2020-03-30 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_settings', '0001_initial'),
        ('catalogue', '0007_product_safe_warning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productingredient',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Κοστος'),
        ),
        migrations.AlterField(
            model_name='productingredient',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_value', to='catalogue.Product', verbose_name='Συστατικο'),
        ),
        migrations.AlterField(
            model_name='productingredient',
            name='qty',
            field=models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Αναλογια'),
        ),
        migrations.AlterField(
            model_name='productstorage',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='project_settings.Storage', verbose_name='Αποθηκη'),
        ),
    ]

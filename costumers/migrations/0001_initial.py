# Generated by Django 2.2 on 2020-03-16 07:08

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project_settings', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Costumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eponimia', models.CharField(max_length=240, null=True, verbose_name='Επωνυμια')),
                ('address', models.CharField(blank=True, max_length=240, null=True, verbose_name='Διευθυνση')),
                ('job_description', models.CharField(blank=True, max_length=240, null=True, verbose_name='Επαγγελμα')),
                ('loading_place', models.CharField(blank=True, default='Εδρα μας', max_length=240, null=True, verbose_name='Τοπος Φορτωσης')),
                ('destination', models.CharField(blank=True, default='Εδρα του,', max_length=240, null=True, verbose_name='Προορισμος')),
                ('afm', models.CharField(blank=True, max_length=10, null=True, verbose_name='ΑΦΜ')),
                ('doy', models.CharField(blank=True, default='Σπαρτη', max_length=240, null=True, verbose_name='ΔΟΥ')),
                ('destination_city', models.CharField(blank=True, max_length=240, null=True, verbose_name='Πολη')),
                ('transport', models.CharField(blank=True, max_length=10, null=True, verbose_name='Μεταφορικο Μεσο')),
                ('first_name', models.CharField(blank=True, max_length=200, verbose_name='Ονομα')),
                ('last_name', models.CharField(blank=True, max_length=200, verbose_name='Επιθετο')),
                ('amka', models.CharField(blank=True, max_length=20, verbose_name='Ψευδονυμο')),
                ('notes', models.CharField(blank=True, max_length=200, verbose_name='Σημειώσεις')),
                ('cellphone', models.CharField(blank=True, max_length=20, verbose_name='Κινητό')),
                ('phone', models.CharField(blank=True, max_length=20, verbose_name='Τηλέφωνο')),
                ('active', models.BooleanField(default=True, verbose_name='Ενεργός')),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('paid_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
            ],
            options={
                'ordering': ['eponimia', 'afm'],
            },
        ),
        migrations.CreateModel(
            name='MyCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorite', models.BooleanField(default=False, verbose_name='Προτεινομενο')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='Τιτλος')),
                ('eponimia', models.CharField(max_length=200, verbose_name='Επωνυμια')),
                ('job', models.TextField(verbose_name='Περιγραφη Επαγγελματος')),
                ('afm', models.CharField(max_length=10, verbose_name='ΑΦΜ')),
                ('doy', models.CharField(max_length=150, verbose_name='ΔΟΥ')),
                ('city', models.CharField(max_length=150, verbose_name='Εδρα')),
                ('zipcode', models.CharField(max_length=10, verbose_name='TK')),
                ('phone', models.CharField(max_length=100, verbose_name='Τηλεφωνα')),
                ('fax', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(choices=[('a', 'Τιμολογιο'), ('b', 'Δελτιο Παραγγελίας'), ('c', 'Προπαραγγελία')], default='a', max_length=1, verbose_name='Ειδος Παραστατικου')),
                ('number', models.IntegerField(blank=True, null=True)),
                ('series', models.CharField(choices=[('a', 'A'), ('b', 'B'), ('c', 'Γ')], max_length=1, verbose_name='Σειρά')),
                ('place', models.CharField(blank=True, max_length=220)),
                ('date', models.DateTimeField(default=datetime.datetime(2020, 3, 16, 7, 8, 50, 129186, tzinfo=utc), verbose_name='Ημερομηνία')),
                ('value', models.DecimalField(decimal_places=2, default=0.0, max_digits=17, verbose_name='Αξια Προ Εκπτωσεως')),
                ('discount_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=17, verbose_name='Εκπτωση')),
                ('clean_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=17, verbose_name='Καθαρη Αξια')),
                ('taxes_value', models.DecimalField(decimal_places=2, default=0.0, max_digits=17, verbose_name='Συνολο ΦΠΑ')),
                ('charges_cost', models.DecimalField(decimal_places=2, default=0.0, max_digits=17, verbose_name='επιβαρυνσεις')),
                ('charges_taxes', models.DecimalField(decimal_places=2, default=0.0, max_digits=17, verbose_name='επιβαρυνσεις ΦΠΑ')),
                ('total_value', models.DecimalField(decimal_places=2, default=0, max_digits=17, verbose_name='Πληρωτεο Ποσο')),
                ('final_value', models.DecimalField(decimal_places=2, default=0, max_digits=17, verbose_name='Τελική Αξία')),
                ('notes', tinymce.models.HTMLField(blank=True, null=True)),
                ('card_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='costumers.MyCard', verbose_name='Στάμπα')),
                ('costumer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='costumers.Costumer', verbose_name='Πελάτης')),
                ('payment_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='project_settings.PaymentMethod', verbose_name='Τρόπος Πληρωμής')),
            ],
            options={
                'ordering': ['-id'],
                'unique_together': {('number', 'series', 'order_type')},
            },
        ),
        migrations.CreateModel(
            name='InvoiceItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Περιγραφη')),
                ('unit', models.CharField(choices=[('a', 'Τεμάχιο'), ('b', 'Κιβώτιο'), ('c', 'Κιλό')], default='a', max_length=1, verbose_name='ΜΜ')),
                ('qty', models.DecimalField(decimal_places=2, default=1, max_digits=17, verbose_name='Ποσότητα')),
                ('value', models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Τιμή')),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Εκπτωση')),
                ('discount_value', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Ποσο Εκπτωσης')),
                ('clean_value', models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Αξια')),
                ('total_clean_value', models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Καθαρη Αξια')),
                ('taxes_modifier', models.IntegerField(default=24, verbose_name='ΦΠΑ')),
                ('taxes_value', models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Αξια ΦΠΑ')),
                ('total_value', models.DecimalField(decimal_places=2, max_digits=17, verbose_name='Τελικη Αξία')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='costumers.PaymentInvoice')),
            ],
        ),
        migrations.CreateModel(
            name='CostumerDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eponimia', models.CharField(max_length=240, null=True, verbose_name='Επωνυμια')),
                ('address', models.CharField(blank=True, max_length=240, null=True, verbose_name='Διευθυνση')),
                ('job_description', models.CharField(blank=True, max_length=240, null=True, verbose_name='Επαγγελμα')),
                ('loading_place', models.CharField(blank=True, default='Εδρα μας', max_length=240, null=True, verbose_name='Τοπος Φορτωσης')),
                ('destination', models.CharField(blank=True, default='Εδρα του,', max_length=240, null=True, verbose_name='Προορισμος')),
                ('afm', models.CharField(blank=True, max_length=10, null=True, verbose_name='ΑΦΜ')),
                ('doy', models.CharField(blank=True, default='Σπαρτη', max_length=240, null=True, verbose_name='ΔΟΥ')),
                ('destination_city', models.CharField(blank=True, max_length=240, null=True, verbose_name='Πολη')),
                ('transport', models.CharField(blank=True, max_length=10, null=True, verbose_name='Μεταφορικο Μεσο')),
                ('phone', models.CharField(blank=True, max_length=200, null=True, verbose_name='Τηλεφωνα')),
                ('costumer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='costumers.Costumer')),
                ('invoice', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='costumers.PaymentInvoice')),
            ],
        ),
    ]

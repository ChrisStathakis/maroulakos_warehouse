from django.test import TestCase

from catalogue.models import ProductClass, ProductStorage, Product
from costumers.models import Costumer
from warehouse.models import Invoice, InvoiceItem, Vendor
from warehouse.warehouse_models import InvoiceTransformation, InvoiceTransformationIngredient, InvoiceTransformationItem
from project_settings.models import Storage
from django.utils import timezone


class TestInvoiceTransformation(TestCase):

    def setUp(self):
        self.product_class_1 = ProductClass.objects.create(have_storage=True, have_ingredient=True, title='Test_1')
        self.product_class_2 = ProductClass.objects.create(have_ingredient=False, have_storage=True, title='test_2')
        self.storage_1 = Storage.objects.create(title='Storage_1', max_capacity=1500, capacity=0,
                                                warning_low_max_capacity=0, warning_max_capacity=0)
        self.storage_2 = Storage.objects.create(title='Storage_2', max_capacity=1500, capacity=0,
                                                warning_low_max_capacity=0, warning_max_capacity=0)

        self.product_1 = Product.objects.create(title='product_1', product_class=self.product_class_1, price=8.00)
        self.product_storage_1 = ProductStorage.objects.create(product=self.product_1, storage=self.storage_1, priority=True)
        self.product_2 = Product.objects.create(title='product_2', product_class=self.product_class_2)
        self.product_storage_2 = ProductStorage.objects.create(product=self.product_2, storage=self.storage_2,
                                                               priority=True, qty=500)
        self.product_3 = Product.objects.create(title='product_3', product_class=self.product_class_2)
        self.product_storage_3 = ProductStorage.objects.create(product=self.product_3, storage=self.storage_2,
                                                               priority=True, qty=500)

        self.vendor = Vendor.objects.create(title='Vendor_1')
        self.invoice = Invoice.objects.create(title='Invoice 1', order_type='a', vendor=self.vendor, date=timezone.now())
        item_1 = InvoiceItem.objects.create(invoice=self.invoice,
                                            product=self.product_2,
                                            storage=self.product_storage_2,
                                            qty=500,
                                            value=0.5,
                                            vendor=self.vendor
                                            )
        item_2 = InvoiceItem.objects.create(invoice=self.invoice, product=self.product_3,
                                            storage=self.product_storage_3,
                                            qty=500,
                                            value=0.2,
                                            vendor=self.vendor
                                            )

    def test_products_qty(self):
        self.assertEqual(self.product_storage_3.qty, 500)
        self.assertEqual(self.product_3.qty, 500)
        self.assertEqual(self.product_2.price_buy, 0.5)

    def test_transform(self):
        costumer = Costumer.objects.create(eponimia='Costumer_1')
        transformation_invoice = InvoiceTransformation.objects.create(date=timezone.now(),
                                                                      costumer=costumer,
                                                                      title='inv_1'
                                                                      )
        transformation_item = InvoiceTransformationItem.objects.create(invoice=transformation_invoice,
                                                                       product=self.product_1,
                                                                       value=self.product_1.final_price,
                                                                       qty=100,
                                                                       storage=self.product_storage_1
                                                                       )

        tran_ingre = InvoiceTransformationIngredient.objects.create(
            invoice_item=transformation_item,
            qty=100,
            product=self.product_2,
            storage=self.product_storage_2,
            cost=0.4
        )

        tran_ingre_1 = InvoiceTransformationIngredient.objects.create(
            invoice_item=transformation_item,
            qty=100,
            product=self.product_3,
            storage=self.product_storage_3,
            cost=0.2
        )

        self.assertEqual(round(tran_ingre.total_cost), 40)
        self.assertEqual(round(tran_ingre.total_cost+tran_ingre_1.total_cost), 60)
        self.assertEqual(transformation_invoice.cost, 60)

        self.assertEqual(self.product_storage_3.qty, 400)
        self.assertEqual(self.product_storage_3.qty, 400)
        self.assertEqual(self.product_storage_1.qty, 100)
        self.assertEqual(self.product_1.qty, 100)



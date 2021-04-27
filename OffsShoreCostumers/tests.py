from django.test import TestCase

from .models import *


class TestCustomerExchanges(TestCase):

    def setUp(self):
        self.company = OffsShoreCompany.objects.create(title='company_1')
        self.costumer = OffsShoreCostumer.objects.create(title='costumer_1')
        self.company_customer = OffsShoreCompanyCostumer.objects.create(
                                                                        costumer=self.costumer,
                                                                        company=self.company
                                                                        )

    def test_orders_and_payments(self):
        new_payment = OffshorePayment.objects.create(
            date=datetime.datetime.now(),
            value=40,
            customer=self.company_customer,
        )
        print('test 1')
        self.assertEqual(-new_payment.value, self.company_customer.balance)
        print('test 2')
        new_payment.delete()
        self.assertEqual(self.company_customer.balance, 0)
        print('3')
        new_order = OffshoreOrder.objects.create(
            customer=self.company_customer,
            value=100,
            date=datetime.datetime.now()
        )
        self.assertEqual(self.company_customer.balance, new_order.value)
        self.assertEqual(self.company.balance, new_order.value)
        print('test 4')




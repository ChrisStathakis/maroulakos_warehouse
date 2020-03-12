import django_tables2 as tables
from .models import ProductClass, Product


class ProductClassTable(tables.Table):

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        model = ProductClass
        fields = ['title', 'have_storage', 'have_ingredient']


class ProductTable(tables.Table):

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        model = Product
        fields = ['sku', 'title', 'product_class__title', 'qty', 'price_buy', 'final_price']

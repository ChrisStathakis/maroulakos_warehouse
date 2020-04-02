import django_tables2 as tables
from .models import ProductClass, Product, Category


class ProductClassTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_edit_url }}'>{{ record }} </a>")

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        model = ProductClass
        fields = ['title', 'have_storage', 'have_ingredient']


class ProductTable(tables.Table):
    title = tables.TemplateColumn("<a href='{{ record.get_edit_url }}'>{{ record }} </a>")
    final_price = tables.Column(verbose_name='Αξια Πωλησης')
    price_buy = tables.Column(verbose_name='Αξια Αγορας')
    product_class__title = tables.Column(verbose_name='Ειδος')
    order_sku = tables.Column(verbose_name='Κωδ. Τιμολ.')

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        model = Product
        fields = ['sku', 'order_sku', 'title', 'product_class__title', 'vendor', 'qty', 'price_buy', 'final_price']


class CategoryTable(tables.Table):
    name = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}'>{{ record }}</a>",
        orderable=False,
    )

    class Meta:
        model = Category
        template_name = 'django_tables2/bootstrap.html'
        fields = ['name', 'parent', ]

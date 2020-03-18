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

    class Meta:
        template_name = 'django_tables2/bootstrap.html'
        model = Product
        fields = ['sku', 'title', 'product_class__title', 'qty', 'price_buy', 'final_price']


class CategoryTable(tables.Table):
    name = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}'>{{ record }}</a>",
        orderable=False,
    )

    class Meta:
        model = Category
        template_name = 'django_tables2/bootstrap.html'
        fields = ['name', 'parent', ]

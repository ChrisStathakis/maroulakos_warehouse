import django_tables2 as tables


from .models import OffsShoreCompany, OffsShoreCostumer, OffsShoreCompanyCostumer, OffshoreOrder, OffshorePayment


class OffsShoreCompanyTable(tables.Table):
    btn = tables.TemplateColumn("<a href='{{ record.get_absolute_url }}' class='btn btn-info'><i class='fa fa-edit'></i> </a>", verbose_name='-')

    class Meta:
        model = OffsShoreCompany
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'btn']


class OffshoreCompanyCostumerTable(tables.Table):
    btn = tables.TemplateColumn(
        "<a href='{{ record.get_absolute_url }}' class='btn btn-info'><i class='fa fa-edit'></i> </a>",
        verbose_name='-')

    class Meta:
        model = OffsShoreCompanyCostumer
        template_name = 'django_tables2/bootstrap.html'
        fields = ['costumer', 'balance', 'btn']


class OrderTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_costumer_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='Επεξεργασια'
    )
    info = tables.TemplateColumn(
        "<button data-href='{{ record.get_modal_url }}' class='btn btn-success btn-round quick_view'>"
        "<i class='fa fa-info'></i></button>",
        orderable=False, verbose_name='Πληροφοριες'
    )
    tag_value = tables.Column(orderable=False, verbose_name='Αξία')

    class Meta:
        model = OffshoreOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'tag_value', 'info', 'action']


class PaymentTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_costumer_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False,verbose_name='Επεξεργασια'
    )
    info = tables.TemplateColumn(
        "<button data-href='{{ record.get_modal_url }}' class='btn btn-success btn-round quick_view'>"
        "<i class='fa fa-info'></i></button>",
        orderable=False, verbose_name='Πληροφοριες'
    )
    tag_value = tables.Column(orderable=False, verbose_name='Αξια')

    class Meta:
        model = OffshorePayment
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'tag_value', 'info', 'action']


class OrderTableListView(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False,verbose_name='Επεξεργασια'
    )
    tag_value = tables.Column(orderable=False, verbose_name='Αξία')

    class Meta:
        model = OffshoreOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'customer', 'title', 'tag_value']


class PaymentTableListView(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='Επεξεργασια'
    )
    tag_value = tables.Column(orderable=False, verbose_name='Αξία')

    class Meta:
        model = OffshorePayment
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'customer', 'title', 'tag_value']
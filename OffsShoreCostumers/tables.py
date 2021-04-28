import django_tables2 as tables


from .models import OffsShoreCompany, OffsShoreCostumer, OffsShoreCompanyCostumer, OffshoreOrder, OffshorePayment


class OffsShoreCompanyTable(tables.Table):
    btn = tables.TemplateColumn("<a href='{{ record.get_absolute_url }}' class='btn btn-info'><i class='fa fa-edit'></i> </a>", verbose_name='-')

    class Meta:
        model = OffsShoreCompany
        template_name = 'django_tables2/bootstrap.html'
        fields = ['title', 'btn']


class OffshoreCompanyCostumerTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='Καρτέλα'
    )


    actions = tables.TemplateColumn(
        '<a href="{{ record.get_order_url }}" class="btn btn-warning btn-round">'
        '<i class="fa fa-plus"> Παραστατικο</i>'
        '</a>'
        , orderable=False, verbose_name='Δημιουργια'
    )

    tag_balance = tables.Column(orderable=False, verbose_name='Υπολοιπο')

    class Meta:
        model = OffsShoreCompanyCostumer
        template_name = 'django_tables2/bootstrap.html'
        fields = ['costumer', 'tag_balance', 'actions', 'action']


class OrderTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='Επεξεργασια'
    )
    info = tables.TemplateColumn(
        "<a href='{{ record.get_delete_url }}' class='btn btn-danger btn-round'>"
        "<i class='fa fa-remove'></i></a>",
        orderable=False, verbose_name='διαγραφη'
    )
    date = tables.TemplateColumn('<p>{{ record.date|date:"d-m-Y" }} </p>', orderable=False, verbose_name='ημερομηνια')
    tag_value = tables.Column(orderable=False, verbose_name='Αξία')

    class Meta:
        model = OffshoreOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'tag_value', 'action', 'info']


class PaymentTable(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='Επεξεργασια'
    )
    info = tables.TemplateColumn(
        "<a href='{{ record.get_delete_url }}' class='btn btn-danger btn-round'>"
        "<i class='fa fa-remove'></i></a>",
        orderable=False, verbose_name='Διαγραφή'
    )
    ate = tables.TemplateColumn('<p>{{ record.date|date:"d-m-Y" }} </p>', orderable=False, verbose_name='ημερομηνια')
    tag_value = tables.Column(orderable=False, verbose_name='Αξια')

    class Meta:
        model = OffshorePayment
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'title', 'tag_value', 'action', 'info']


class OrderTableListView(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='Επεξεργασια'
    )
    info = tables.TemplateColumn(
        "<a href='{{ record.get_delete_url }}' class='btn btn-danger btn-round'>"
        "<i class='fa fa-remove'></i></button>",
        orderable=False, verbose_name='Διαγραφή'
    )
    tag_value = tables.Column(orderable=False, verbose_name='Αξία')

    class Meta:
        model = OffshoreOrder
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'customer', 'title', 'tag_value', 'action', 'info']


class PaymentTableListView(tables.Table):
    action = tables.TemplateColumn(
        "<a href='{{ record.get_edit_url }}' class='btn btn-primary btn-round'><i class='fa fa-edit'></i></a>",
        orderable=False, verbose_name='Επεξεργασια'
    )
    info = tables.TemplateColumn(
        "<a href='{{ record.get_delete_url }}' class='btn btn-danger btn-round'>"
        "<i class='fa fa-remove'></i></button>",
        orderable=False, verbose_name='Διαγραφή'
    )
    tag_value = tables.Column(orderable=False, verbose_name='Αξία')

    class Meta:
        model = OffshorePayment
        template_name = 'django_tables2/bootstrap.html'
        fields = ['date', 'customer', 'title', 'tag_value', 'action', 'info']

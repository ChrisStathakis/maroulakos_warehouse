from django import forms
from .models import Vendor, Note, VendorBankingAccount, Invoice, Payment, Product, InvoiceItem, ProductStorage
from .warehouse_models import InvoiceTransformation, InvoiceTransformationItem


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class VendorForm(BaseForm, forms.ModelForm):
    site = forms.URLField(widget=forms.TextInput(), required=False)

    class Meta:
        model = Vendor
        fields = ['active', 'title', 'owner', 'afm', 'doy', 'phone', 'cellphone', 'address', 'email', 'site', 'taxes_modifier']

    def clean_site(self):
        data = self.cleaned_data.get('site', None)
        if data:
            if not 'http' in data:
                data = 'https://'+ data
        return data


class InvoiceVendorDetailForm(BaseForm, forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label='Ημερομηνία')

    class Meta:
        model = Invoice
        fields = ['date', 'title', 'vendor', 'value', 'extra_value', 'payment_method', 'description']


class InvoiceForm(BaseForm, forms.ModelForm):
    # vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label='Ημερομηνία')

    class Meta:
        model = Invoice
        fields = '__all__'


class PaymentForm(BaseForm, forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput())
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = Payment
        fields = '__all__'


class VendorBankingAccountForm(BaseForm, forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = VendorBankingAccount
        fields = '__all__'


class NoteForm(BaseForm, forms.ModelForm):
    vendor_related = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput())
     #text = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 200}))

    class Meta:
        model = Note
        fields = ['status', 'title', 'text', 'vendor_related']


class InvoiceProductForm(BaseForm, forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput(), required=True)

    class Meta:
        model = Product
        fields = ['order_sku', 'title', 'unit', 'taxes_modifier', 
                  'order_discount', 'product_class', 'vendor', 'price_buy',
                  
                  ]


class InvoiceItemForm(BaseForm, forms.ModelForm):
    vendor = forms.ModelChoiceField(queryset=Vendor.objects.all(), widget=forms.HiddenInput())
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.all(), widget=forms.HiddenInput())
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = InvoiceItem
        fields = ['order_code', 'unit', 'qty', 'value', 'discount',
                  'taxes_modifier', 'storage', 'vendor', 'invoice', 'product'
                  ]


class InvoiceTransformationForm(BaseForm, forms.ModelForm):
    date = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = InvoiceTransformation
        fields = ['date', 'title', 'costumer', 'payment_method']


class InvoiceTransformationItemForm(BaseForm, forms.ModelForm):
    # storage = forms.ModelChoiceField(queryset=ProductStorage.objects.all(), widget=forms.HiddenInput(), required=False)
    invoice = forms.ModelChoiceField(queryset=InvoiceTransformation.objects.all(), widget=forms.HiddenInput())
    product = forms.ModelChoiceField(queryset=Product.objects.all(), widget=forms.HiddenInput())

    class Meta:
        model = InvoiceTransformationItem
        fields = ['invoice', 'product', 'storage', 'qty', 'value', ]

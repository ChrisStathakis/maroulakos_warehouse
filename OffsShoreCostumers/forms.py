from django import forms

from .models import OffsShoreCompany, OffsShoreCompanyCostumer, OffshoreOrder, OffshorePayment, OffsShoreCostumer


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class OffshoreCompanyForm(BaseForm, forms.ModelForm):

    class Meta:
        model = OffsShoreCompany
        fields = '__all__'


class OffshoreCostumerForm(BaseForm, forms.ModelForm):

    class Meta:
        model = OffsShoreCostumer
        fields = '__all__'


class OffshoreOrderForm(BaseForm, forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=OffsShoreCompanyCostumer.objects.all(), widget=forms.HiddenInput())
    date = forms.DateField(label='Ημερομηνία', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = OffshoreOrder
        fields = '__all__'


class OffshorePaymentForm(BaseForm, forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=OffsShoreCompanyCostumer.objects.all(), widget=forms.HiddenInput())
    date = forms.DateField(label='Ημερομηνία', widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = OffshorePayment
        fields = '__all__'
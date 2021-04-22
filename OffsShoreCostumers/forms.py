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
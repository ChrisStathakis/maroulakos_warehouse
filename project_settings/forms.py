from django import forms

from .models import Storage, PaymentMethod


class BaseForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class StorageForm(BaseForm, forms.ModelForm):

    class Meta:
        model = Storage
        fields = ['title', 'active']


class PaymentMethodForm(BaseForm, forms.ModelForm):

    class Meta:
        model = PaymentMethod
        fields = '__all__'
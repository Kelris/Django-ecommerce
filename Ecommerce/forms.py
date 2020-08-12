from django import forms
from Accounts.models import Address


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):                                                                                # https://docs.djangoproject.com/en/3.0/ref/forms/widgets/#styling-widget-instances
        super().__init__(*args, **kwargs)

        # self.fields['address_type'].widget = forms.RadioSelect(choices=self.fields['address_type'].widget.choices)
        self.fields['address_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address type'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last name'})
        self.fields['address_line_1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address (line 1)'})
        self.fields['address_line_2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Address (line 2)'})
        self.fields['postal_code'].widget.attrs.update({'class': 'form-control', 'placeholder': 'ZIP'})
        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'City'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'placeholder': 'State'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Country'})

    class Meta:
        model = Address
        fields = [
            'address_type',
            'first_name',
            'last_name',
            'address_line_1',
            'address_line_2',
            'postal_code',
            'city',
            'state',
            'country',
        ]


from django.test import TestCase

# Create your tests here.
from Ecommerce.forms import AddressForm


class TestAddressForm(TestCase):
    def test_form_fields(self):
        form = AddressForm()
        form_fields = [
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

        self.assertEquals(form._meta.fields, form_fields)

    def test_valid_data(self):
        form = AddressForm(data={
            'address_type':     'shipping',
            'first_name':       'John',
            'last_name':        'Smith',
            'address_line_1':   '3000 North Street',
            'address_line_2':   '',
            'postal_code':      '99501',
            'city':             'Flynn',
            'state':            'TX',
            'country':          'USA',
        })

        self.assertTrue(form.is_valid())

    def test_required_fields(self):
        data = {
            'address_type':     '',
            'first_name':       '',
            'last_name':        '',
            'address_line_1':   '',
            # 'address_line_2':   '', # not required
            'postal_code':      '',
            'city':             '',
            # 'state':            '', # not required
            'country':          '',
        }

        form = AddressForm(data)

        for key in data:
            self.assertEquals(form.errors[key], ['This field is required.'])

    def test_widget_attrs(self):
        form = AddressForm()
        widget_attrs_list = [
            ('address_type', {'class': 'form-control', 'placeholder': 'Address type'}),
            ('first_name', {'maxlength': '30', 'class': 'form-control', 'placeholder': 'First name'}),
            ('last_name', {'maxlength': '120', 'class': 'form-control', 'placeholder': 'Last name'}),
            ('address_line_1', {'maxlength': '120', 'class': 'form-control', 'placeholder': 'Address (line 1)'}),
            ('address_line_2', {'maxlength': '120', 'class': 'form-control', 'placeholder': 'Address (line 2)'}),
            ('postal_code', {'maxlength': '16', 'class': 'form-control', 'placeholder': 'ZIP'}),
            ('city', {'maxlength': '120', 'class': 'form-control', 'placeholder': 'City'}),
            ('state', {'maxlength': '120', 'class': 'form-control', 'placeholder': 'State'}),
            ('country', {'maxlength': '120', 'class': 'form-control', 'placeholder': 'Country'}),
        ]

        for line in widget_attrs_list:
            self.assertEquals(form.fields[line[0]].widget.attrs, line[1])

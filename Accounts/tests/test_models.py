from django.test import TestCase

# Create your tests here.
from Accounts.models import Customer, Address
from Ecommerce.models import Order
import datetime


class TestCustomer(TestCase):

    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(name="John")

# Testing field labels (verbose names):

    def test_field_labels(self):
        customer = Customer.objects.get(name="John")

        labels_list = [
            ('user', 'user'),
            ('name', 'name'),
            ('email', 'email'),
        ]

        for label in labels_list:
            field_label = customer._meta.get_field(label[0]).verbose_name
            self.assertEquals(field_label, label[1])

# Testing field options

    def test_name_max_length(self):
        customer = Customer.objects.get(name="John")
        max_length = customer._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)


class TestAddress(TestCase):
    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(name="John")
        customer = Customer.objects.get(name="John")

        Order.objects.create(date_ordered=datetime.datetime, completed=False, transaction_id='666')
        order = Order.objects.get(completed=False)

        Address.objects.create(first_name="John", customer=customer, order=order)

# Testing field labels (verbose names):

    def test_field_labels(self):
        address = Address.objects.get(first_name="John")

        labels_list = [
            ('customer', 'customer'),
            ('order', 'order'),
            ('address_type', 'address type'),
            ('last_name', 'last name'),
            ('address_line_1', 'address line 1'),
            ('address_line_2', 'address line 2'),
            ('postal_code', 'postal code'),
            ('city', 'city'),
            ('state', 'state'),
            ('country', 'country'),
        ]

        for label in labels_list:
            field_label = address._meta.get_field(label[0]).verbose_name
            self.assertEquals(field_label, label[1])

# Testing field options

    def test_ADDRESS_TYPES(self):
        address = Address.objects.get(first_name="John")
        address_types = [
            ('billing', 'Billing'),
            ('shipping', 'Shipping')
        ]
        self.assertEquals(address.ADDRESS_TYPES, address_types)

    def test_address_customer_relation(self):
        customer = Customer.objects.get(name="John")
        address = Address.objects.get(customer=customer)
        self.assertEquals(address.customer.name, "John")

    def test_address_order_relation(self):
        order = Order.objects.get(completed=False)
        address = Address.objects.get(order=order)
        self.assertEquals(address.order.transaction_id, '666')

    def test_address_type_choices_field(self):
        address = Address.objects.get(first_name="John")
        address_types = [
            ('billing', 'Billing'),
            ('shipping', 'Shipping')
        ]
        self.assertEquals(address._meta.get_field('address_type').choices, address_types)

    def test_first_name_max_length(self):
        address = Address.objects.get(first_name="John")
        max_length = address._meta.get_field('first_name').max_length
        self.assertEquals(max_length, 30)

    def test_last_name_max_length(self):
        address = Address.objects.get(first_name="John")
        max_length = address._meta.get_field('last_name').max_length
        self.assertEquals(max_length, 120)

    def test_address_line_1_max_length(self):
        address = Address.objects.get(first_name="John")
        max_length = address._meta.get_field('address_line_1').max_length
        self.assertEquals(max_length, 120)

    def test_address_line_2_max_length(self):
        address = Address.objects.get(first_name="John")
        max_length = address._meta.get_field('address_line_2').max_length
        self.assertEquals(max_length, 120)

    def test_postal_code_max_length(self):
        address = Address.objects.get(first_name="John")
        max_length = address._meta.get_field('postal_code').max_length
        self.assertEquals(max_length, 16)

    def test_city_max_length(self):
        address = Address.objects.get(first_name="John")
        max_length = address._meta.get_field('city').max_length
        self.assertEquals(max_length, 120)

    def test_state_max_length(self):
        address = Address.objects.get(first_name="John")
        max_length = address._meta.get_field('state').max_length
        self.assertEquals(max_length, 120)

    def test_country_max_length(self):
        address = Address.objects.get(first_name="John")
        max_length = address._meta.get_field('country').max_length
        self.assertEquals(max_length, 120)

# Testing model methods

    def test_verbose_name_plural(self):
        address = Address.objects.get(first_name="John")
        self.assertEquals(address._meta.verbose_name_plural, 'Addresses')

    def test_string_representation(self):
        address = Address.objects.get(first_name="John")
        str_representation = str(address.customer) + ' : ' + str(address.address_type).upper()
        self.assertEquals(str(address), str_representation)

    def test_get_address(self):
        address = Address.objects.get(first_name="John")
        get_address = f"{address.address_line_1} {address.address_line_2 or ''} / {address.state}, {address.postal_code} {address.city} {address.country}"
        self.assertEquals(address.get_address(), get_address)

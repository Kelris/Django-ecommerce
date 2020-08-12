from django.test import TestCase

# Create your tests here.
from Ecommerce.models import Product, Order, OrderProduct
from Accounts.models import Customer
import datetime


class TestProduct(TestCase):

    @classmethod
    def setUpTestData(cls):
        Product.objects.create(name="Kalarepa", price=10)

# Testing field labels (verbose names):

    def test_field_labels(self):
        product = Product.objects.get(name="Kalarepa")

        labels_list = [
            ('name', 'name'),
            ('price', 'price'),
            ('description', 'description'),
            ('image', 'image'),
        ]
        for label in labels_list:
            field_label = product._meta.get_field(label[0]).verbose_name
            self.assertEquals(field_label, label[1])

# Testing field options

    def test_name_max_length(self):
        product = Product.objects.get(name="Kalarepa")
        max_length = product._meta.get_field('name').max_length
        self.assertEquals(max_length, 100)

    def test_price_max_digits(self):
        product = Product.objects.get(name="Kalarepa")
        max_digits = product._meta.get_field('price').max_digits
        self.assertEquals(max_digits, 6)

    def test_price_decimal_places(self):
        product = Product.objects.get(name="Kalarepa")
        decimal_places = product._meta.get_field('price').decimal_places
        self.assertEquals(decimal_places, 2)

# Testing model methods

    def test_product_string_representation(self):
        product = Product.objects.get(name="Kalarepa")
        str_representation = str(product.name) + ' ' + str(product.price) + " €"
        self.assertEquals(str_representation, str(product))


class TestOrder(TestCase):

    @classmethod
    def setUpTestData(cls):
        customer = Customer.objects.create(name="John")
        Order.objects.create(customer=customer, date_ordered=datetime.datetime, completed=False)
        Product.objects.create(name="Kalarepa", price=10)

# Testing field labels (verbose names):

    def test_field_labels(self):
        order = Order.objects.get(completed=False)

        labels_list = [
            ('customer', 'customer'),
            ('transaction_id', 'transaction id'),
            ('date_ordered', 'date ordered'),
            ('completed', 'completed'),
        ]
        for label in labels_list:
            field_label = order._meta.get_field(label[0]).verbose_name
            self.assertEquals(field_label, label[1])

# Testing field options

    def test_order_customer_relation(self):
        order = Order.objects.get(completed=False)
        self.assertEquals(order.customer.name, "John")

    def test_transaction_id_max_length(self):
        order = Order.objects.get(completed=False)
        transaction_id = order._meta.get_field('transaction_id').max_length
        self.assertEquals(transaction_id, 200)

# Testing model methods

    def test_order_string_representation(self):
        order = Order.objects.get(completed=False)
        str_representation = str(order.id)
        self.assertEquals(str_representation, str(order))

    def test_cart_total_price(self):
        order = Order.objects.get(completed=False)
        product = Product.objects.get(name="Kalarepa")
        OrderProduct.objects.create(order=order, product=product, quantity=1, date_added=datetime.datetime)

        total_price = order.cart_total_price
        self.assertEquals(total_price, 10)

    def test_cart_total_items(self):
        order = Order.objects.get(completed=False)
        product = Product.objects.get(name="Kalarepa")
        OrderProduct.objects.create(order=order, product=product, quantity=1, date_added=datetime.datetime)
        OrderProduct.objects.create(order=order, product=product, quantity=2, date_added=datetime.datetime)

        total_items = order.cart_total_items
        self.assertEquals(total_items, 3)


class TestOrderProduct(TestCase):

    @classmethod
    def setUpTestData(cls):
        Customer.objects.create(name="John")

        customer = Customer.objects.get(name="John")
        Order.objects.create(customer=customer, completed=False, date_ordered=datetime.datetime)

        order = Order.objects.get(customer=customer)
        Product.objects.create(name="Kalarepa", price=10)

        product = Product.objects.get(name="Kalarepa", price=10)
        OrderProduct.objects.create(order=order, product=product, quantity=1, date_added=datetime.datetime)

# Testing field labels (verbose names):

    def test_field_labels(self):
        orderproduct = OrderProduct.objects.get(quantity=1)

        labels_list = [
            ('order', 'order'),
            ('product', 'product'),
            ('quantity', 'quantity'),
            ('date_added', 'date added'),
        ]

        for label in labels_list:
            label_field = orderproduct._meta.get_field(label[0]).verbose_name
            self.assertEquals(label_field, label[1])

# Testing field options

    def test_orderproduct_order_relation(self):
        order = Order.objects.get(completed=False)
        orderproduct = OrderProduct.objects.get(order=order)
        self.assertEquals(orderproduct.order.customer.name, "John")

    def test_orderproduct_product_relation(self):
        product = Product.objects.get(name="Kalarepa")
        orderproduct = OrderProduct.objects.get(product=product)
        self.assertEquals(orderproduct.product.name, "Kalarepa")

# Testing model methods

    def test_orderproduct_string_representation(self):
        orderproduct = OrderProduct.objects.get(quantity=1)
        str_representation = str(orderproduct.product) + " x " + str(orderproduct.quantity)
        self.assertEquals(str(orderproduct), str_representation)

    def test_verbose_name_plural(self):
        orderproduct = OrderProduct.objects.get(quantity=1)
        label_field_plural = orderproduct._meta.verbose_name_plural
        self.assertEquals(label_field_plural, 'OrderProducts')

    def test_product_total_price(self):
        customer = Customer.objects.get(name="John")
        order = Order.objects.get(customer=customer)
        product = Product.objects.get(name="Kalarepa")

        OrderProduct.objects.create(order=order, product=product, quantity=3)
        orderproduct = OrderProduct.objects.get(quantity=3)

        self.assertEquals(orderproduct.product_total_price, 30)


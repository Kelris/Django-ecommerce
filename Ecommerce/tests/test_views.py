from django.test import TestCase

# Create your tests here.
from django.urls import reverse


class TestIndexView(TestCase):
    def test_url_pattern_GET(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_url_name_GET(self):
        response = self.client.get(reverse('index'))
        self.assertEquals(response.status_code, 200)

    def test_template_GET(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'Ecommerce/index.html')

    def test_context_GET(self):
        response = self.client.get(reverse('index'))
        self.assertIn('order', response.context)


class TestStoreView(TestCase):
    def test_url_pattern_GET(self):
        response = self.client.get('/store/')
        self.assertEquals(response.status_code, 200)

    def test_url_name_GET(self):
        response = self.client.get(reverse('store'))
        self.assertEquals(response.status_code, 200)

    def test_template_GET(self):
        response = self.client.get(reverse('store'))
        self.assertTemplateUsed(response, 'Ecommerce/store.html')

    def test_context_GET(self):
        response = self.client.get(reverse('store'))
        self.assertIn('products', response.context)
        self.assertIn('order', response.context)
        self.assertIn('orderproducts', response.context)


class TestCheckoutView(TestCase):
    def test_url_pattern_GET(self):
        response = self.client.get('/checkout/')
        self.assertEquals(response.status_code, 200)

    def test_url_name_GET(self):
        response = self.client.get(reverse('checkout'))
        self.assertEquals(response.status_code, 200)

    def test_template_GET(self):
        response = self.client.get(reverse('checkout'))
        self.assertTemplateUsed(response, 'Ecommerce/checkout.html')

    def test_context_GET(self):
        response = self.client.get(reverse('checkout'))
        self.assertIn('order', response.context)
        self.assertIn('orderproducts', response.context)
        self.assertIn('form', response.context)

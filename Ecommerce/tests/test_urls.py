from django.test import TestCase, SimpleTestCase

# Create your tests here.
from Ecommerce.views import IndexView, StoreView, UpdateItemView, CheckoutView, ProcessOrderView
from django.urls import reverse, resolve


class TestUrls(SimpleTestCase):

    # def test_list_url_is_resolved(self):
    #     url = reverse('index')                                                                                        # returns URL based on 'name' --> https://docs.djangoproject.com/en/3.0/ref/urlresolvers/#reverse
    #     print(resolve(url))                                                                                           # returns view connected with URL --> https://docs.djangoproject.com/en/3.0/ref/urlresolvers/#resolve
    #     self.assertEquals(resolve(url).func.__name__, IndexView.__name__)                                             # https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.Response.resolver_match

    def test_list_urls_is_resolved(self):
        """Checks if the URL matches the view."""
        test_urls_list = [
            ('/', IndexView),
            ('/store/', StoreView),
            ('/update_item/', UpdateItemView),
            ('/checkout/', CheckoutView),
            ('/process_order/', ProcessOrderView),
        ]

        for url in test_urls_list:
            self.assertEqual(resolve(url[0]).func.view_class, url[1])

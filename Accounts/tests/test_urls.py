from django.test import TestCase, SimpleTestCase

# Create your tests here.
from django.urls import resolve

from Accounts.views import register, login_view, change_account
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    # def test_list_url_is_resolved(self):
    #     url = reverse('index')                                                                                          # zwraca URL na podstawie 'name' --> https://docs.djangoproject.com/en/3.0/ref/urlresolvers/#reverse
    #     print(resolve(url))                                                                                           # zwraca widok związany z danym URL --> https://docs.djangoproject.com/en/3.0/ref/urlresolvers/#resolve
    #     self.assertEquals(resolve(url).func.__name__, IndexView.__name__)                                               # https://docs.djangoproject.com/en/3.1/topics/testing/tools/#django.test.Response.resolver_match

    def test_list_urls_is_resolved(self):
        """Checks if the URL matches the view."""
        test_urls_func_list = [
            ('/users/register/', register),
            ('/users/login/', login_view),
            ('/users/change_account/', change_account),
        ]

        for url in test_urls_func_list:
            self.assertEqual(resolve(url[0]).func, url[1])

        test_urls_class_list = [
            ('/users/logout/', auth_views.LogoutView),
        ]
        for url in test_urls_class_list:
            self.assertEqual(resolve(url[0]).func.view_class, url[1])


from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from django.contrib.auth.models import User


class TestRegisterView(TestCase):
    def test_url_pattern_GET(self):
        response = self.client.get('/users/register/')
        self.assertEquals(response.status_code, 200)

    def test_url_name_GET(self):
        response = self.client.get(reverse('register'))
        self.assertEquals(response.status_code, 200)

    def test_template_GET(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'Accounts/register.html')

    def test_context_GET(self):
        response = self.client.get(reverse('register'))
        self.assertIn('form', response.context)


class TestLoginView(TestCase):
    def setUp(self):
        # Create two users
        User.objects.create_user(username='john_smith', password='test123*')

    def test_url_pattern_GET(self):
        response = self.client.get('/users/login/')
        self.assertEquals(response.status_code, 200)

    def test_url_name_GET(self):
        response = self.client.get(reverse('login_view'))
        self.assertEquals(response.status_code, 200)

    def test_template_GET(self):
        response = self.client.get(reverse('login_view'))
        self.assertTemplateUsed(response, 'Accounts/login.html')

    def test_context_GET(self):
        response = self.client.get(reverse('login_view'))
        self.assertIn('form', response.context)

    def test_logging_process(self):
        self.client.login(username='john_smith', password='test123*')

        response = self.client.get(reverse('index'))

        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'john_smith')

        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)


class TestLogoutView(TestCase):
    def test_url_pattern_GET(self):
        response = self.client.get('/users/logout/')
        self.assertEquals(response.status_code, 200)

    def test_url_name_GET(self):
        response = self.client.get(reverse('logout'))
        self.assertEquals(response.status_code, 200)

    def test_template_GET(self):
        response = self.client.get(reverse('logout'))
        self.assertTemplateUsed(response, 'Accounts/logout.html')


class TestChangeAccountView(TestCase):
    def test_url_pattern_GET(self):
        response = self.client.get('/users/change_account/')
        self.assertEquals(response.status_code, 200)

    def test_url_name_GET(self):
        response = self.client.get(reverse('change_account'))
        self.assertEquals(response.status_code, 200)

    def test_template_GET(self):
        response = self.client.get(reverse('change_account'))
        self.assertTemplateUsed(response, 'Accounts/change_account.html')

    def test_context_GET(self):
        response = self.client.get(reverse('change_account'))
        self.assertIn('register_form', response.context)
        self.assertIn('login_form', response.context)

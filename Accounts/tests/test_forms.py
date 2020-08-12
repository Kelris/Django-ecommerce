from django.contrib.auth.models import User
from django.test import TestCase

# Create your tests here.
from Accounts.forms import UserCreationForm, AuthenticationForm


class TestUserCreationForm(TestCase):
    def test_required_fields(self):
        data = {
            'username':     '',
            'password1':    '',
            'password2':    '',
            'email':        '',
        }

        form = UserCreationForm(data)

        for key in data:
            self.assertEquals(form.errors[key], ['This field is required.'])

    def test_valid_data(self):
        form = UserCreationForm(data={
            'username':     'john_smith',
            'password1':    'test123*',
            'password2':    'test123*',
            'email':        'jsmith@gmail.com',
        })

        self.assertTrue(form.is_valid())

    def test_redirects_to_index(self):
        response = self.client.post('/users/register/', data={'username': 'john_smith', 'password1': 'test123*', 'password2': 'test123*', 'email': 'jsmith@gmail.com'}, follow=True)

        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 200)

    def test_invalid_password(self):
        form = UserCreationForm(data={
            'username':     'john_smith',
            'password1':    'test123*',
            'password2':    'test1234**',
            'email':        'jsmith@gmail.com',
        })

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors["password2"], ['The two password fields didn’t match.'])                           # self.assertEqual(form["password2"].errors, [str(form.error_messages['password_mismatch'])])


class TestAuthenticationForm(TestCase):
    def setUp(self):
        User.objects.create_user(username='john_smith', password='test123*')

    def test_login(self):
        response = self.client.post('/users/login/', data={'username': 'john_smith', 'password': 'test123*'}, follow=True)

        self.assertEqual(str(response.context['user']), 'john_smith')
        self.assertRedirects(response, '/')
        self.assertEqual(response.status_code, 200)


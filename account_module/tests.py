from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from account_module.forms import LoginForm
from account_module.models import CustomUser


# Create your tests here.


class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = CustomUser.objects.create_user(username=self.username, password=self.password)

    def test_get_login_view(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/login.html')
        self.assertIsInstance(response.context['login_form'], LoginForm)

    def test_post_login_view_with_valid_credentials(self):
        login_data = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_url, data=login_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_module/index.html')
        self.assertTrue(response.context['user'].is_authenticated)

    def test_post_login_view_with_invalid_data(self):
        login_data = {'username': self.username, 'password': 'wrong_password'}
        response = self.client.post(self.login_url, data=login_data, )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/login.html')
        self.assertFormError(response, 'login_form', 'username', 'invalid username or password')
        self.assertFalse(response.context['user'].is_authenticated)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.logout_url = reverse('logout')
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@test.com'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password,
                                                         email=self.email)

    def test_logout_view(self):
        # Log in the user
        self.client.login(username=self.username, password=self.password)

        # Make a GET request to the logout view
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account_module/login.html')
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertRedirects(response, self.login_url)

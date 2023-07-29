from django.contrib.auth import get_user_model
from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import AnonymousUser
from home_module.views import IndexPageView


# Create your tests here.


# class IndexViewTest(TestCase):
#     def setUp(self):
#         self.client = Client()
#         self.login_url = reverse('login')
#         self.index_url = reverse('index_page')
#         self.username = 'testuser'
#         self.password = 'testpassword'
#         self.email = 'test@test.com'
#         self.user = get_user_model().objects.create_user(username=self.username, password=self.password,
#                                                          email=self.email)
#         self.client.login(username=self.username, password=self.password)
#
#     def test_index_view(self):
#         response = self.client.get(self.index_url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'home_module/index.html')
#         self.assertTrue(response.context['user'].is_authenticated)


class TestIndexView(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='root', password='rootpass', email='root@email.com')
        self.factory = RequestFactory()

    def test_index_user_authenticated(self):
        request = self.factory.get(reverse('index_page'))
        request.user = self.user
        response = IndexPageView.as_view()(request)

        self.assertEqual(response.status_code, 200)  # renders index page

    def test_index_user_anonymous(self):
        request = self.factory.get(reverse('index_page'))
        request.user = AnonymousUser()
        response = IndexPageView.as_view()(request)
        self.assertEqual(response.status_code, 302)  # redirects to login page



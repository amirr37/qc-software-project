from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


# Create your tests here.


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('login')
        self.index_url = reverse('index_page')
        self.username = 'testuser'
        self.password = 'testpassword'
        self.email = 'test@test.com'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password,
                                                         email=self.email)
        self.client.login(username=self.username, password=self.password)

    def test_index_view(self):
        # Log in the user
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home_module/index.html')
        self.assertTrue(response.context['user'].is_authenticated)

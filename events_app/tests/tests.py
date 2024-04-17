from rest_framework import status
from .info import superuser_data, category_data
from rest_framework.test import force_authenticate, APIRequestFactory
from rest_framework.test import APIClient
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from users_app.models import User, Token
from users_app.urls import user_login
from ..models import City, Category


class EventsTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username='super_ilya',
                                                   email='pp@ya.ru',
                                                   password='qwerty')
        self.token_url = "/api/token/"
        response = self.client.post(self.token_url, superuser_data, format='json')
        self.token = Token.objects.create(user_id=self.admin,
                                          access_token=response.data.get("access"),
                                          refresh_token=response.data.get("refresh"))
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_create_and_get_city(self):
        url = '/api/v1/categories/'
        # response = self.client.get(url, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = category_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(Category.objects.count(), 1)
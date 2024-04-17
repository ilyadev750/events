from rest_framework import status
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework.test import APITestCase
from ..models import User, Token


class UserTests(APITestCase):
    
    def setUp(self):
        url = reverse('register')
        data = {
            'username': 'ilya_rs',
            'first_name': 'Илья',
            'last_name': 'Петров',
            'email': 'rs@ya.ru',
            'password': 'qwerty',
            }
        register_response = self.client.post(url, data, format='json')

        url_2 = reverse('login')
        data_2 = {
            'username': 'ilya_rs',
            'password': 'qwerty'
        }
        login_response = self.client.post(url_2, data_2, format='json')

    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'ilya_rss',
            'first_name': 'Илья',
            'last_name': 'Петров',
            'email': 'rs@ya.rus',
            'password': 'qwerty',
            }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Token.objects.count(), 1)


    def test_login_user(self):
        url = reverse('login')
        data = {
            'username': 'ilya_rs',
            'password': 'qwerty',
            }
        user = authenticate(username=data['username'], password=data['password'])
        self.assertEqual(User.objects.count(), 1)
from rest_framework import status
from .info import (superuser_login, user_data_registration,
                   event_list_data, user_login, user_data_wrong_password,
                   user_data_exist_user, user_login_wrong_password, bad_token)
from django.urls import reverse
from django.contrib.auth import authenticate
from rest_framework.test import APITestCase
from events_app.models import EventList
from ..models import User, Token


class UserTests(APITestCase):
    
    def setUp(self):
        self.admin = User.objects.create_superuser(username='super_ilya',
                                                   password='qwerty',
                                                   first_name='Илья',
                                                   last_name='Иванов',
                                                   email='www@leningrad.ru')
        self.login_url = reverse("login")
        self.registration_url = reverse("register")
        self.logout_url = reverse("logout")
        self.event_list_url = "/api/v1/events-list/"
        self.event_registration_url = "/api/v1/events-registration/"
        self.refresh_token_url = reverse("user-refresh-token")
        self.event_list_data = event_list_data
        self.user_data_registration = user_data_registration
        self.user_login_data = user_login

        self.client.post(self.login_url, superuser_login, format='json')
        token = Token.objects.get(user_id=self.admin)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token.access_token}'
            )
        self.client.post(self.event_list_url, self.event_list_data, format='json')
        admin_event = self.client.get(f'{self.event_list_url}1/', format='json')
        registration_data = {
            "event_list_id": admin_event.data,
            "user_id": {
                "first_name": "Илья",
                "last_name": "Иванов",
                "email": "www@leningrad.ru"
            },
            "is_registered": "True"
        }
        self.client.post(
            self.event_registration_url,
            registration_data,
            format='json'
            )

        
        self.client.post(self.registration_url, self.user_data_registration, format='json')
        self.client.post(self.login_url, self.user_login_data, format='json')
        token = Token.objects.get(user_id=2)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {token.access_token}'
            )
        
    def test_failed_register_wrong_password(self):
        data = user_data_wrong_password
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_failed_register_exist_user(self):
        data = user_data_exist_user
        response = self.client.post(self.registration_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_wrong_password(self):
        data = user_login_wrong_password
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.data, {"Ошибка": "Неверное имя пользователя или пароль"})

    def test_logout_user_bad_token(self):
        data = bad_token
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.data, {'Ошибка': 'Неверный Refresh токен'})

    def test_logout_user_bad_token(self):
        data = {}
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(response.data, {'Ошибка': 'Необходим Refresh токен'})
    
    def test_successfull_logout(self):
        admin = User.objects.get(username='super_ilya')
        admin_token = Token.objects.get(user_id=admin)
        data = {"refresh_token": f'{admin_token.refresh_token}'}
        response = self.client.post(self.logout_url, data, format='json')
        self.assertEqual(Token.objects.count(), 1)
        self.assertEqual(response.data, {'Успех': 'Выход из системы произведен'})

    def test_success_registration_to_event(self):
        event = self.client.get(f'{self.event_list_url}1/', format='json')
        registration_data = {
            "event_list_id": event.data,
            "user_id": {
                "first_name": "Илья",
                "last_name": "Петров",
                "email": "rs@ya.ru"
            },
            "is_registered": "True"
        }
        registration = self.client.post(
             self.event_registration_url,
             registration_data,
             format='json'
             )
        self.assertEqual(
            registration.status_code, status.HTTP_201_CREATED
            )
        
    def test_failed_registration(self):
        event = self.client.get(f'{self.event_list_url}1/', format='json')
        registration_data = {
            "event_list_id": event.data,
            "user_id": {
                "first_name": "Илья",
                "last_name": "Иванов",
                "email": "www.leningrad.ru"
            },
            "is_registered": "True"
        }
        registration = self.client.post(
             self.event_registration_url,
             registration_data,
             format='json'
             )
        self.assertEqual(
            registration.data, {'Ошибка': "Неверный пользователь"}
            )
        
    def test_cancel_registration_to_event(self):
        event = self.client.get(f'{self.event_list_url}1/', format='json')
        registration_data = {
            "event_list_id": event.data,
            "user_id": {
                "first_name": "Илья",
                "last_name": "Петров",
                "email": "rs@ya.ru"
            },
            "is_registered": "True"
        }
        registration = self.client.post(
             self.event_registration_url,
             registration_data,
             format='json'
             )
        cancel_registration = self.client.delete(
            f'{self.event_registration_url}2/', format='json')
        self.assertEqual(
            cancel_registration.data,
            {"Успех": "Вы успешно отменили запись на данное событие!"}
            )
        
    def test_failed_cancel_another_user_registration(self):
        cancel_registration = self.client.delete(
            f'{self.event_registration_url}1/', format='json'
            )
        self.assertEqual(
            cancel_registration.data,
            {"Ошибка": "Вы не зарегистрированы на данное событие!"}
            )
        
    def test_not_exist_registration(self):
        not_exist_registration = self.client.get(
            self.event_registration_url, format='json'
            )
        self.assertEqual(
            not_exist_registration.data,
            []
            )
        
    def test_refresh_token(self):
        token = Token.objects.get(user_id=2)
        data = {
            'refresh_token': token.refresh_token
        }
        response = self.client.post(
            self.refresh_token_url, data, format='json'
        )
        self.assertEqual(
            response.data.pop('Успех'),
            'Access token обновлен'
            )
        
    def test_wrong_refresh_token(self):
        data = {
            'refresh_token': 'Место для токена'
        }
        response = self.client.post(
            self.refresh_token_url, data, format='json'
        )
        self.assertEqual(
            response.data.pop('Ошибка'),
            'Неверный Refresh токен'
            )
from rest_framework import status
from .info import (superuser_data, category_data,
                   city_data, event_data, location_data,
                   location_data_changed, event_list_data,
                   event_list_data_changed)
from rest_framework.test import APITestCase
from users_app.models import User, Token
from ..models import City, Category, Event, Location, EventList


class EventsTests(APITestCase):

    def setUp(self):
        self.admin = User.objects.create_superuser(username='super_ilya',
                                                   email='pp@ya.ru',
                                                   password='qwerty')
        self.token_url = "/api/token/"
        response = self.client.post(
            self.token_url, superuser_data, format='json'
            )
        self.token = Token.objects.create(
            user_id=self.admin,
            access_token=response.data.get("access"),
            refresh_token=response.data.get("refresh")
            )
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}'
            )

    def test_crud_category(self):

        url = '/api/v1/categories/'
        data = category_data
        self.client.post(url, data, format='json')
        category_get = self.client.get(f'{url}1/', format='json')
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category_get.data.get("category_name"), "Пьеса")


        data["category_name"] = "Мюзикл"
        category_put = self.client.put(f'{url}1/', data, format='json')
        self.assertEqual(category_put.data.get("category_name"), "Мюзикл")


        category_delete = self.client.delete(f'{url}1/', format='json')
        self.assertEqual(
            category_delete.status_code, status.HTTP_204_NO_CONTENT
            )

    def test_crud_city(self):

        url = '/api/v1/cities/'
        data = city_data
        self.client.post(url, data, format='json')
        city_get = self.client.get(f'{url}1/', format='json')
        self.assertEqual(City.objects.count(), 1)
        self.assertEqual(city_get.data.get("city")['city_name'], "Москва")


        data["city_name"] = "Санкт-Петербург"
        city_put = self.client.put(f'{url}1/', data, format='json')
        self.assertEqual(city_put.data.get("city")['city_name'], "Санкт-Петербург")


        city_delete = self.client.delete(f'{url}1/', format='json')
        self.assertEqual(city_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_event(self):

        url = '/api/v1/events/'
        data = event_data
        self.client.post(url, data, format='json')
        event_get = self.client.get(f'{url}1/', format='json')
        self.assertEqual(Event.objects.count(), 1)
        self.assertEqual(event_get.data.get('event_name'), "Бал вампиров")


        data["event_name"] = "Анна Каренина"
        event_put = self.client.put(f'{url}1/', data, format='json')
        self.assertEqual(event_put.data.get("event_name"), "Анна Каренина")
        event_delete = self.client.delete(f'{url}1/', format='json')
        self.assertEqual(event_delete.status_code, status.HTTP_204_NO_CONTENT)

    def test_crud_location(self):
        
        url = '/api/v1/locations/'
        data = location_data
        self.client.post(url, data, format='json')
        location_get = self.client.get(f'{url}1/', format='json')
        self.assertEqual(Location.objects.count(), 1)
        self.assertEqual(
            location_get.data.get('location_name'), "Московский Дом Молодежи"
            )
        self.assertEqual(location_get.data.get('city_id')['city_name'], "Москва")


        data = location_data_changed
        location_put = self.client.put(f'{url}1/', data, format='json')
        self.assertEqual(
            location_put.data.get('location')['location_name'],
            "Стадион Газпром Арена"
            )
        self.assertEqual(
            location_put.data.get('location')['city_id']['city_name'],
            "Санкт-Петербург"
            )

        location_delete = self.client.delete(f'{url}1/', format='json')
        self.assertEqual(location_delete.status_code,
                         status.HTTP_204_NO_CONTENT)
        self.assertEqual(Location.objects.count(), 0)

    def test_crud_eventlist(self):

        event_list_url = '/api/v1/events-list/'
        self.client.post(event_list_url, event_list_data, format='json')
        event_list_get = self.client.get(f'{event_list_url}1/', format='json')
        self.assertEqual(EventList.objects.count(), 1)
        self.assertEqual(
            event_list_get.data['category_id']['category_name'],
            'Пьеса')
        self.assertEqual(
            event_list_get.data['price'],
            3000)
        self.assertEqual(
            event_list_get.data['location_id']['city_id']['city_name'],
            'Москва')

        event_list_put = self.client.put(
            f'{event_list_url}1/', event_list_data_changed, format='json'
            )
        self.assertEqual(
            event_list_put.data['event']['category_id']['category_name'],
            'Мюзикл'
            )
        self.assertEqual(
            event_list_put.data['event']['price'],
            2000
            )
        self.assertEqual(
            event_list_put.data['event']['location_id']['city_id']['city_name'],
            'Санкт-Петербург'
        )


        event_list_delete = self.client.delete(
            f'{event_list_url}1/', format='json'
            )
        self.assertEqual(event_list_delete.status_code,
                         status.HTTP_204_NO_CONTENT)

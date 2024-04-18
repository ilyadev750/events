from rest_framework import serializers
from .models import Category, City, Location, Event, EventList


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории"""
    class Meta:
        model = Category
        fields = "__all__"


class CitySerializer(serializers.ModelSerializer):
    """Сериализатор города"""
    class Meta:
        model = City
        fields = "__all__"

    def create(self, validated_data):
        """Создать город"""
        return City.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Обновить город"""
        instance.city_name = validated_data.get(
            "city_name", instance.city_name
            )
        instance.save()
        return instance


class LocationSerializer(serializers.ModelSerializer):
    """Сериализатор локации"""
    city_id = CitySerializer(many=False)

    class Meta:
        model = Location
        fields = ["city_id", "location_name"]

    def create(self, validated_data):
        """Создать локацию"""
        city_id = validated_data.pop('city_id')
        city, created = City.objects.get_or_create(**city_id)
        location = Location.objects.create(city_id=city, **validated_data)
        return location

    def update(self, instance, validated_data):
        """Обновить локацию"""
        city_id = validated_data.pop('city_id')
        instance.location_name = validated_data.get(
            'location_name', instance.location_name
            )
        city, created = City.objects.get_or_create(**city_id)
        instance.city_id = city
        instance.save()
        return instance


class EventSerializer(serializers.ModelSerializer):
    """Сериализатор события"""
    class Meta:
        model = Event
        fields = "__all__"


class EventListSerializer(serializers.ModelSerializer):
    """Сериализатор списка событий"""
    event_id = EventSerializer(many=False)
    category_id = CategorySerializer(many=False)
    location_id = LocationSerializer(many=False)

    class Meta:
        model = EventList
        fields = "__all__"

    def create(self, validated_data):
        """Создать событие"""
        event_id = validated_data.pop('event_id')
        category_id = validated_data.pop('category_id')
        location_id = validated_data.pop('location_id')
        city_id = location_id.pop('city_id')
        event, created = Event.objects.get_or_create(**event_id)
        category, created = Category.objects.get_or_create(**category_id)
        city, created = City.objects.get_or_create(**city_id)
        location, created = Location.objects.get_or_create(
            city_id=city, **location_id
            )
        new_event = EventList.objects.create(event_id=event,
                                             category_id=category,
                                             location_id=location,
                                             **validated_data)
        return new_event

    def update(self, instance, validated_data):
        """Обновить событие"""
        event_id = validated_data.pop('event_id')
        category_id = validated_data.pop('category_id')
        location_id = validated_data.pop('location_id')
        city_id = location_id.pop('city_id')

        event, created = Event.objects.get_or_create(**event_id)
        category, created = Category.objects.get_or_create(**category_id)
        city, created = City.objects.get_or_create(**city_id)
        location, created = Location.objects.get_or_create(
            city_id=city, **location_id
            )
        location.city_id = city
        location.save()

        instance.event_id = event
        instance.category_id = category
        instance.location_id = location
        instance.date = validated_data.get('date', instance.date)
        instance.time = validated_data.get('time', instance.time)
        instance.price = validated_data.get('price', instance.price)
        instance.save()

        return instance

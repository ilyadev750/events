from django.contrib.auth.models import User
from .models import EventRegistration
from events_app.models import EventList, Event, Category, City, Location
from rest_framework import serializers
from events_app.serializers import EventListSerializer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EventRegistrationSerializer(serializers.ModelSerializer):
    event_list_id = EventListSerializer(many=False)
    user_id = UserEventSerializer(many=False)

    class Meta:
        model = EventRegistration
        fields = "__all__"

    def create(self, validated_data):
        event_list_id = validated_data.pop('event_list_id')
        user_id = validated_data.pop('user_id')
        event = event_list_id.pop('event_id')
        event = Event.objects.get(**event)

        category = event_list_id.pop('category_id')
        category = Category.objects.get(**category)

        location_id = event_list_id.pop('location_id')
        city = location_id.pop('city_id')
        city = City.objects.get(**city)
        location = Location.objects.get(city_id=city, **location_id)

        event_list = EventList.objects.get(event_id=event,
                                           category_id=category,
                                           location_id=location,
                                           **event_list_id)

        user = User.objects.get(**user_id)

        event_registration = EventRegistration.objects.create(
            event_list_id=event_list,
            user_id=user,
            is_registered=True)

        return event_registration

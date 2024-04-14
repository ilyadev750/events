from rest_framework import serializers 
from .models import Category, City, Location, Event, EventList


class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = "__all__"

       
class CitySerializer(serializers.ModelSerializer):
    class Meta: 
        model = City
        fields = "__all__"

    def create(self, validated_data):
        return City.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.city_name = validated_data.get("city_name", instance.city_name)
        instance.save()
        return instance
    

class LocationSerializer(serializers.ModelSerializer):
    city_id = CitySerializer(many=False)
    class Meta: 
        model = Location
        fields = ["city_id", "location_name"]

    def create(self, validated_data):
        city_id = validated_data.pop('city_id')
        city, created = City.objects.get_or_create(**city_id)
        location = Location.objects.create(city_id=city, **validated_data)
        return location


class EventSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Event
        fields = "__all__"

class EventListSerializer(serializers.ModelSerializer):
    event_id = EventSerializer(many=True)
    category_id = CategorySerializer(many=True)
    location_id = LocationSerializer(many=True)

    class Meta: 
        model = Event
        fields = "__all__"